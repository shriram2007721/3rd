import unittest
import threading


class RideSystem:

    def __init__(self):

        self.vehicles = {
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

        self.drivers = {
            "Bike": ["Driver1"],
            "Sedan": ["Driver2"],
            "SUV": ["Driver3"],
            "Premium": ["Driver4"]
        }

        self.lock = threading.Lock()

    # Fare Calculation
    def calculate_fare(
            self,
            distance,
            passengers,
            vehicle,
            booking_time,
            discount=0):

        if distance <= 0:
            return "Invalid distance"

        if passengers <= 0:
            return "Invalid passenger count"

        if vehicle not in self.vehicles:
            return "Invalid vehicle"

        if passengers > self.vehicles[vehicle]["max_passengers"]:
            return "Excessive passengers"

        if booking_time < 0 or booking_time > 23:
            return "Invalid booking time"

        base = self.vehicles[vehicle]["base"]
        rate = self.vehicles[vehicle]["rate"]

        fare = base + distance * rate

        # Passenger surcharge
        if passengers > 1:
            fare += (passengers - 1) * 20

        # Peak surcharge
        if (7 <= booking_time <= 10) or \
           (17 <= booking_time <= 20):

            fare *= 1.25

        # Night surcharge
        if booking_time >= 22 or booking_time < 5:

            fare *= 1.15

        # Maximum discount = 50
        if discount > 50:
            discount = 50

        if discount < 0:
            discount = 0

        fare -= discount

        if fare < 0:
            fare = 0

        return round(fare, 2)

    # Driver Allocation
    def assign_driver(self, vehicle):

        if vehicle not in self.drivers:
            return None

        if len(self.drivers[vehicle]) == 0:
            return None

        return self.drivers[vehicle][0]

    # Booking
    def book(self, distance, passengers,
              vehicle, booking_time, discount=0):

        fare = self.calculate_fare(
            distance,
            passengers,
            vehicle,
            booking_time,
            discount
        )

        if isinstance(fare, str):
            return fare

        driver = self.assign_driver(vehicle)

        if driver is None:
            return "Driver unavailable"

        return fare


class RideBookingQA(unittest.TestCase):

    def setUp(self):

        self.ride = RideSystem()

    # 1. Normal Booking
    def test_normal_booking(self):

        result = self.ride.book(
            10,
            2,
            "Sedan",
            14,
            0
        )

        self.assertGreater(result, 0)

    # 2. Peak Hour Booking
    def test_peak_hour_booking(self):

        normal = self.ride.book(
            10,
            1,
            "Sedan",
            14,
            0
        )

        peak = self.ride.book(
            10,
            1,
            "Sedan",
            8,
            0
        )

        self.assertGreater(
            peak,
            normal
        )

    # 3. Night Booking
    def test_night_booking(self):

        normal = self.ride.book(
            10,
            1,
            "Sedan",
            14,
            0
        )

        night = self.ride.book(
            10,
            1,
            "Sedan",
            23,
            0
        )

        self.assertGreater(
            night,
            normal
        )

    # 4. Invalid Distance
    def test_invalid_distance(self):

        result = self.ride.book(
            0,
            1,
            "Sedan",
            14,
            0
        )

        self.assertEqual(
            result,
            "Invalid distance"
        )

    # 5. Invalid Passenger Count
    def test_invalid_passenger_count(self):

        result = self.ride.book(
            10,
            0,
            "Sedan",
            14,
            0
        )

        self.assertEqual(
            result,
            "Invalid passenger count"
        )

    # 6. Unavailable Driver
    def test_unavailable_driver(self):

        self.ride.drivers["SUV"] = []

        result = self.ride.book(
            10,
            2,
            "SUV",
            14,
            0
        )

        self.assertEqual(
            result,
            "Driver unavailable"
        )

    # 7. Maximum Discount
    def test_maximum_discount(self):

        result = self.ride.book(
            10,
            1,
            "Bike",
            14,
            1000
        )

        expected = 30 + (10 * 10) - 50

        self.assertEqual(
            result,
            expected
        )

    # 8. Multiple Vehicle Types
    def test_multiple_vehicle_types(self):

        bike = self.ride.book(
            10,
            1,
            "Bike",
            14,
            0
        )

        sedan = self.ride.book(
            10,
            1,
            "Sedan",
            14,
            0
        )

        suv = self.ride.book(
            10,
            1,
            "SUV",
            14,
            0
        )

        premium = self.ride.book(
            10,
            1,
            "Premium",
            14,
            0
        )

        self.assertGreater(bike, 0)
        self.assertGreater(sedan, 0)
        self.assertGreater(suv, 0)
        self.assertGreater(premium, 0)

    # 9. Boundary Fare Value
    def test_boundary_fare(self):

        result = self.ride.book(
            0.1,
            1,
            "Bike",
            14,
            0
        )

        self.assertGreater(
            result,
            0
        )

    # 10. Driver Allocation Logic
    def test_driver_allocation(self):

        driver = self.ride.assign_driver(
            "SUV"
        )

        self.assertEqual(
            driver,
            "Driver3"
        )

    # 11. Excessive Passengers
    def test_excessive_passengers(self):

        result = self.ride.book(
            10,
            5,
            "Sedan",
            14,
            0
        )

        self.assertEqual(
            result,
            "Excessive passengers"
        )

    # 12. Invalid Booking Time
    def test_invalid_booking_time(self):

        result = self.ride.book(
            10,
            2,
            "Sedan",
            25,
            0
        )

        self.assertEqual(
            result,
            "Invalid booking time"
        )


if __name__ == "__main__":

    unittest.main(verbosity=2)
