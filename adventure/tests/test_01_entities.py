from datetime import date

import pytest

from django.core.exceptions import ValidationError

from adventure import models


@pytest.fixture
def car():
    return models.VehicleType(max_capacity=4)


@pytest.fixture
def van():
    return models.VehicleType(max_capacity=6)


@pytest.fixture
def tesla(car):
    return models.Vehicle(
        name="Tesla", passengers=3, vehicle_type=car, number_plate="AA-12-34"
    )

@pytest.fixture
def service_area_center():
    return models.ServiceArea(
        kilometer=60, gas_price=894
    )

@pytest.fixture
def service_area_left():
    return models.ServiceArea(
        kilometer=40, gas_price=894
    )

@pytest.fixture
def service_area_right():
    return models.ServiceArea(
        kilometer=90, gas_price=894
    )


class TestVehicle:
    def test_capacity_greater_than_passengers(self, car):
        vehicle = models.Vehicle(vehicle_type=car, passengers=2)
        assert vehicle.can_start()

    def test_vehicle_overload(self, car):
        vehicle = models.Vehicle(vehicle_type=car, passengers=10)
        assert not vehicle.can_start()

    def test_vehicle_distribution(self, car, van):
        vehicle = models.Vehicle(vehicle_type=car, passengers=3)
        distribution_expected = [[True, True], [True, False]]
        assert vehicle.get_distribution() == distribution_expected

        vehicle = models.Vehicle(vehicle_type=van, passengers=5)
        distribution_expected = [[True, True], [True, True], [True, False]]
        assert vehicle.get_distribution() == distribution_expected

    @pytest.mark.parametrize(
        "p_number_plate, expected",
        [
        ("AA-12-34", True),
        ("AA-BB-34", False),
        ("12-34-56", False),
        ("AA1234", True),
        ("AA 12 34", True)
        ]
    )
    def test_valid_number_plate(self, p_number_plate, expected):
        # TODO: implement a function called "validate_number_plate"
        # a valid number plate consists of three pairs of alphanumeric chars separated by hyphen
        # the first pair must be letters and the rest must be numbers
        # e.g: AA-12-34
        vehicle = models.Vehicle(number_plate=p_number_plate)
        assert vehicle.validate_number_plate() == expected

class TestServiceArea:
    def test_wrong_left_placement(self, service_area_center, service_area_right):
        station = service_area_center
        station.left_station = service_area_right

        with pytest.raises(ValidationError):
            service_area_center.clean()

    def test_wrong_right_placement(self, service_area_center, service_area_left):
        station = service_area_center
        station.right_station = service_area_left

        with pytest.raises(ValidationError):
            service_area_center.clean()


class TestJourney:
    def test_is_finished(self, tesla):
        journey = models.Journey(start=date.today(), end=date.today(), vehicle=tesla)
        assert journey.is_finished()

    def test_is_not_finished(self, tesla):
        journey = models.Journey(start=date.today(), vehicle=tesla)
        assert not journey.is_finished()
