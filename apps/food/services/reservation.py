import datetime

from rest_framework.exceptions import ValidationError

from apps.food.models import TableReservation


def validate_reservation_time(request):
    data = {
        'restaurant_id': request.user.current_restaurant.id,
        'time_of_start': request.data.get('time_of_start'),
        'table_id': request.data.get('table'),
        'time_of_end':
            request.data.get('time_of_end') if request.data.get('time_of_end') else
            TableReservation.add_default_reservation_time(
                datetime.datetime.fromisoformat(request.data.get('time_of_start'))
            )
    }
    reserved_times_count = TableReservation.objects.filter(restaurant_id=data['restaurant_id'],
                                                           table_id=data['table_id']).count()
    if reserved_times_count:
        time_free = TableReservation.objects.raw('''
            with
                reserved_times as (
                    select
                    time_of_start as current_start,
                    time_of_end as current_end,
                    LAG(time_of_start) OVER (partition by food_tablereservation.table_id ORDER BY food_tablereservation.time_of_start desc) AS next_start,
                    LAG(time_of_start) OVER (partition by food_tablereservation.table_id ORDER BY food_tablereservation.time_of_start asc) AS prev_start
                    from food_tablereservation
                    where food_tablereservation.restaurant_id = %(restaurant_id)s and food_tablereservation.table_id = %(table_id)s
                    order by current_end desc
                )
            select 1 as id, reserved_times.* from reserved_times
            where
                (
                    (%(time_of_start)s between reserved_times.current_end and reserved_times.next_start)
                        and
                    (%(time_of_end)s between reserved_times.current_end and reserved_times.next_start)
                )
                or
                (
                    %(time_of_start)s > reserved_times.current_end and next_start is null
                )
                or
                (
                    %(time_of_end)s < reserved_times.current_start and prev_start is null
                )
                ''', data)
        if not time_free:
            avaliable_time_range = TableReservation.objects.raw('''
                select
                1 as id,
                food_table.number,
                time_of_start as current_start,
                time_of_end as current_end,
                LAG(time_of_start) OVER (partition by food_tablereservation.table_id ORDER BY food_tablereservation.time_of_start desc) AS next_start,
                LAG(time_of_start) OVER (partition by food_tablereservation.table_id ORDER BY food_tablereservation.time_of_start asc) AS prev_start
                from food_tablereservation
                join food_table on food_tablereservation.table_id = food_table.id
                where food_tablereservation.restaurant_id = %(restaurant_id)s
                and (date(time_of_start) = date(%(time_of_start)s) or date(time_of_end) = date(%(time_of_end)s))
                order by food_table.number, current_start asc
                ''', data)
            result = {}
            for row in avaliable_time_range:
                if row.number not in result.keys():
                    result[row.number] = []

                if not row.prev_start and not row.next_start:
                    available_time = f'available - {row.current_start}'
                    result[row.number].append(available_time)
                    available_time = f'{row.current_end} - available'
                    result[row.number].append(available_time)
                elif not row.next_start:
                    available_time = f'{row.current_end} - available'
                    result[row.number].append(available_time)
                elif not row.prev_start:
                    available_time = f'available - {row.current_start}'
                    result[row.number].append(available_time)
                    if row.next_start:
                        if str(row.current_end) == str(row.next_start):
                            continue
                        available_time = f'{row.current_end} - {row.next_start}'
                        result[row.number].append(available_time)
                        continue
                else:
                    if str(row.current_end) == str(row.next_start):
                        continue
                    available_time = f'{row.current_end} - {row.next_start}'
                    result[row.number].append(available_time)

            raise ValidationError(
                {
                    'time': 'current time range unavailable',
                    'available times': 'if table number dont show below - all time available',
                    **result
                }
            )
