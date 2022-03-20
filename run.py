import time
from luno.functions import lunoFunctions

lf = lunoFunctions()
frequency = lf.loop_frequency()
price = lf.price()
averages = lf.init_average(price)
mode = lf.get_mode()
order = lf.get_order()
delay = lf.start_delay()

while True:
    price = lf.price()
    if price == 0:
        pass
    else:
        averages = lf.update_averages(averages, price)
        average = lf.get_average(averages)
        minimum_price = min(averages)
        maximum_price = max(averages)
        print("Price: " + str(price) + " Average: " + str(average) + " Min: " + str(minimum_price) + " Max: " + str(maximum_price))
        if mode == 0:
            pass
        elif delay > 0:
            delay = delay - 1
        elif mode == 1:
            order = lf.buyer(price, average, minimum_price, maximum_price)
            if order != "N/A":
                lf.store_order_id(order)
                mode = lf.update_mode(3)
        elif mode == 2:
            order = lf.seller(price, average, minimum_price, maximum_price)
            if order != "N/A":
                lf.store_order_id(order)
                mode = lf.update_mode(3)
            else:
                mode = 1
        else:
            mode = lf.check_order(order, mode, minimum_price)
        time.sleep(frequency)


