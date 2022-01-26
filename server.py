import math
import random
import sys

Q_LIMIT = 100
BUSY = 1
IDLE = 0
sim_time = 0.0
time_last_event = 0.0
server_status = 0
num_in_q = 0
total_of_delays = 0.0
num_custs_delayed = 0

time_next_event = [0] * 3
time_arrival = [0] * int(Q_LIMIT)
mean_service = 0.0
num_custs_delayed = 0
next_event_type = 0
num_events = 0
area_num_in_q = 0.0
area_server_status = 0.0


# Initialization function.
def initialize(mean_interarrival):
    print("Initialize")
    global time_next_event, sim_time, num_in_q, server_status, time_last_event, num_custs_delayed, total_of_delays, area_num_in_q, area_server_status
    sim_time = 0.0
    # initialize the state variables
    server_status = IDLE
    num_in_q = 0
    time_last_event = 0.0

    # initialize the statistical counters.
    num_custs_delayed = 0
    total_of_delays = 0.0
    area_num_in_q = 0.0
    area_server_status = 0.0

    # Initialize event list. Since no customers are present, the departure(service completion) event is eliminated from consideration.

    time_next_event[1] = sim_time + expon(mean_interarrival)
    time_next_event[2] = pow(10, 30)


# Timing function
def timing(num_events):
    print("Timing")
    global sim_time, next_event_type

    min_time_next_event = pow(10, 29)
    next_event_type = 0

    # Determine the event type of the next event to occur.

    for i in range(1, num_events + 1):
        print(min_time_next_event)
        if time_next_event[i] < min_time_next_event:
            min_time_next_event = time_next_event[i]
            next_event_type = i
        print(i)
        print(min_time_next_event)
    print(next_event_type)
    # Check to see whether the event list is empty.
    if next_event_type == 0:
        # The event list is empty, so stop the simulation.
        with open('Output.txt', 'w') as outfile:
            outfile.write(f"Event list empty at time {sim_time}\n\n")
        sys.exit()

    # The event list is not empty, so advance the simulation clock.
    sim_time = min_time_next_event


def arrive(mean_interarrival, mean_service):
    print("Arrive")
    global server_status
    global total_of_delays
    global num_custs_delayed
    global time_arrival
    global num_in_q

    delay = float

    # Schedule next arrival.
    time_next_event[1] = sim_time + expon(mean_interarrival)

    # Check to see whether server is busy.

    if server_status == BUSY:
        # Server is busy, so increment number of customers in queue.
        num_in_q += 1

        # Check to see whether an overflow condition exists.
        if num_in_q > Q_LIMIT:
            num_in_q = Q_LIMIT
        if num_in_q > Q_LIMIT:
            # The queue has overflowed, so stop the simulation.
            with open('Output.txt', 'w') as outfile:
                outfile.write(f"Overflow of array time_interval at time {sim_time}\n\n")

        # There is still room in the queue, so store the time of arrival of the
        # arriving customer at the (new) end of time_arrival.
        print(num_in_q)
        print(len(time_arrival))
        time_arrival[num_in_q - 1] = sim_time


    else:
        # Server is idle, so arriving customer has a delay of zero. (The
        # following two statements are for program clarity and do not affect
        # the results of the simulation.)
        delay = 0.0
        total_of_delays += delay

        # Increment the number of customers delayed, and make server busy.
        num_custs_delayed += 1
        server_status = BUSY

        # Schedule a departure (service completion).
        time_next_event[2] = sim_time + expon(mean_service)


def depart():
    print("depart")
    global total_of_delays, num_in_q, num_custs_delayed, server_status

    delay = float

    # Check to see whether the queue is empty.
    if num_in_q == 0:
        # The queue is empty so make the server idle and eliminate the
        # departure (service completion) event from consideration.
        server_status = IDLE
        time_next_event[2] = pow(10, 30)
    else:
        # The queue is nonempty, so decrement the number of customers in queue.
        num_in_q -= 1

        # Compute the delay of the customer who is beginning service and update the total delay accumulator.
        delay = sim_time - time_arrival[1]
        total_of_delays += delay

        # Increment the number of customers delayed, and schedule departure.
        num_custs_delayed += 1
        print(num_custs_delayed)
        time_next_event[2] = sim_time + expon(mean_service)

        # Move each customer in queue (if any) up one place.

        for i in range(1, num_in_q):
            time_arrival[i] = time_arrival[i + 1]


# Report generator function.
def report(num_delays_required):
    print("report")
    # Compute and write estimates of desired measures of performance.
    with open('Output.txt', 'w') as outfile:
        outfile.write("Single-server queueing system \n\n")
        outfile.write(f"Mean interarrival time {mean_interarrival} minutes \n\n")
        outfile.write(f"Mean service time {mean_service} minutes \n\n")
        outfile.write(f"Number of customers {num_delays_required} \n\n")
        outfile.write(f"Average delay in queue  {total_of_delays / num_custs_delayed:.2f} minutes\n\n")
        outfile.write(f"Average number in queue  {area_num_in_q / sim_time:.3f} \n\n")
        outfile.write(f"Server utilization  {area_server_status / sim_time:.3f} \n\n")
        outfile.write(f"Time simulation ended  {sim_time:.3f} minutes \n\n")


# Update area accumulators for time-average statistics.
def update_time_average_stats():
    global time_last_event
    global area_num_in_q
    global area_server_status
    global num_in_q

    # Compute time since last event, and update last-event-time marker.
    time_since_last_event = sim_time - time_last_event
    time_last_event = sim_time

    # Update area under number-in-queue function.
    area_num_in_q += num_in_q * time_since_last_event
    # Update area under server-busy indicator function.
    area_server_status += server_status * time_since_last_event


# Exponential variate generation function.
def expon(mean):
    # Return an exponential random variate with mean "mean".

    return -mean * math.log(random.random())


def main():
    global mean_service, num_custs_delayed, mean_interarrival
    num_custs_delayed = 0

    # Open and read input file
    with open('../../Downloads/Input.txt', 'r') as infile:
        res = infile.read()

        mean_interarrival = float(res[:3])

        mean_service = float(res[4:7])

        num_delays_required = float(res[8:])

    # Open output file
    # Write report heading and input parameters.
    with open('Output.txt', 'w') as outfile:
        outfile.write("Single-server queueing system \n\n")
        outfile.write(f"Mean interarrival time {mean_interarrival} minutes \n\n")
        outfile.write(f"Mean service time {mean_service} minutes \n\n")
        outfile.write(f"Number of customers {num_delays_required} \n\n")
    # Specify number of events for the timing function.
    num_events = 2

    # Initialize the simulation.
    initialize(mean_interarrival)

    # Run the simulation while more delays are still needed.

    while num_custs_delayed < num_delays_required:
        # Determine the next event.
        timing(num_events)

        # Update time-average statistical accumulators.
        update_time_average_stats()

        # Invoke the appropri

        if next_event_type == 1:

            arrive(mean_interarrival, mean_service)
        elif next_event_type == 2:
            depart()
    # Invoke the report generator and end of simulation.
    print("call report")
    report(num_delays_required)



if __name__ == '__main__':
    main()
