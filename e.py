from datetime import datetime


class RideBooking:

    VEHICLE_RATES = {
        "Bike": 10,
        "Sedan": 15,
        "SUV": 20,
        "Premium": 30
    }

    MAX_PASSENGERS = {
        "Bike": 1,
        "Sedan": 4,
        "SUV": 6,
        "Premium": 4
    }

    DRIVERS = {
        "Bike": ["Driver1", "Driver2"],
        "Sedan": ["Driver3", "Driver4"],
        "SUV": ["Driver5"],
        "Premium": ["Driver6"]
    }

    def __init__(self):

        self.base_fare = {
            "Bike": 30,
            "Sedan": 50,
            "SUV": 80,
            "Premium": 120
        }

        self.peak_charge = 1.25
        self.night_charge = 1.15
        self.passenger_charge = 20
        self.max_discount = 50

    # Validate Booking
    def validate_booking(
            self,
            distance,
            passengers,
            vehicle,
            booking_time):

        if distance <= 0:
            return "Invalid distance"

        if vehicle not in self.VEHICLE_RATES:
            return "Invalid vehicle"

        if passengers <= 0:
            return "Invalid passenger count"

        if passengers > self.MAX_PASSENGERS[vehicle]:
            return "Excessive passengers"

        if not isinstance(booking_time, int):
            return "Invalid booking time"

        if booking_time < 0 or booking_time > 23:
            return "Invalid booking time"

        return "Valid"

    # Driver Allocation
    def assign_driver(self, vehicle):

        if vehicle not in self.DRIVERS:
            return None

        if len(self.DRIVERS[vehicle]) == 0:
            return None

        return self.DRIVERS[vehicle][0]

    # Calculate Fare
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

        # Base fare
        fare = self.base_fare[vehicle]

        # Distance fare
        fare += distance * self.VEHICLE_RATES[vehicle]

        # Passenger surcharge
        if passengers > 1:
            fare += (passengers - 1) * self.passenger_charge

        # Peak hour: 7-10 AM and 5-8 PM
        if (7 <= booking_time <= 10) or \
           (17 <= booking_time <= 20):

            fare *= self.peak_charge

        # Night: 10 PM - 5 AM
        if booking_time >= 22 or booking_time < 5:
            fare *= self.night_charge

        # Maximum discount
        if discount < 0:
            discount = 0

        if discount > self.max_discount:
            discount = self.max_discount

        fare -= discount

        if fare < 0:
            fare = 0

        return round(fare, 2)

    # Complete Booking
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
            "vehicle": vehicle,
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
