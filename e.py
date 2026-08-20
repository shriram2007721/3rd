from datetime import datetime


class RideBooking:

    VEHICLES = {
        "Bike": {
            "base": 30,
            "rate": 10,
            "max_passengers": 1
        },
        "Sedan": {
            "base": 50,
            "rate": 15,
            "max_passengers": 4
        },
        "SUV": {
            "base": 80,
            "rate": 20,
            "max_passengers": 6
        },
        "Premium": {
            "base": 120,
            "rate": 30,
            "max_passengers": 4
        }
    }

    def __init__(self):

        self.drivers = {
            "Bike": ["Driver1", "Driver2"],
            "Sedan": ["Driver3", "Driver4"],
            "SUV": ["Driver5"],
            "Premium": ["Driver6"]
        }

        self.maximum_discount = 50

    # Validate Booking
    def validate_booking(
            self,
            distance,
            passengers,
            vehicle,
            booking_time):

        if distance <= 0:
            return "Invalid distance"

        if vehicle not in self.VEHICLES:
            return "Invalid vehicle"

        if passengers <= 0:
            return "Invalid passenger count"

        maximum = self.VEHICLES[vehicle]["max_passengers"]

        if passengers > maximum:
            return "Excessive passengers"

        if booking_time < 0 or booking_time > 23:
            return "Invalid booking time"

        return "Valid"

    # Driver Allocation
    def assign_driver(self, vehicle):

        if vehicle not in self.drivers:
            return None

        if len(self.drivers[vehicle]) == 0:
            return None

        return self.drivers[vehicle][0]

    # Fare Calculation
    def calculate_fare(
            self,
            distance,
            passengers,
            vehicle,
            booking_time,
            discount=0):

        validation = self.validate_booking(
            distance,
            passengers,
            vehicle,
            booking_time
        )

        if validation != "Valid":
            return validation

        base = self.VEHICLES[vehicle]["base"]
        rate = self.VEHICLES[vehicle]["rate"]

        # Base fare + distance fare
        fare = base + (distance * rate)

        # Passenger surcharge
        if passengers > 1:
            fare += (passengers - 1) * 20

        # Peak hour surcharge
        if (7 <= booking_time <= 10) or \
           (17 <= booking_time <= 20):

            fare *= 1.25

        # Night surcharge
        if booking_time >= 22 or booking_time < 5:

            fare *= 1.15

        # Maximum discount
        if discount < 0:
            discount = 0

        if discount > self.maximum_discount:
            discount = self.maximum_discount

        fare -= discount

        if fare < 0:
            fare = 0

        return round(fare, 2)

    # Complete Ride Booking
    def book_ride(
            self,
            customer_id,
            pickup,
            drop,
            distance,
            passengers,
            vehicle,
            booking_time,
            discount=0):

        validation = self.validate_booking(
            distance,
            passengers,
            vehicle,
            booking_time
        )

        if validation != "Valid":

            return {
                "status": "FAILED",
                "message": validation
            }

        driver = self.assign_driver(vehicle)

        if driver is None:

            return {
                "status": "FAILED",
                "message": "Driver unavailable"
            }

        fare = self.calculate_fare(
            distance,
            passengers,
            vehicle,
            booking_time,
            discount
        )

        return {
            "status": "SUCCESS",
            "customer_id": customer_id,
            "pickup": pickup,
            "drop": drop,
            "distance": distance,
            "passengers": passengers,
            "vehicle": vehicle,
            "booking_time": booking_time,
            "driver": driver,
            "fare": fare
        }


if __name__ == "__main__":

    ride = RideBooking()

    result = ride.book_ride(
        "C001",
        "VIT",
        "Katpadi",
        10,
        2,
        "Sedan",
        14,
        20
    )

    print(result)
