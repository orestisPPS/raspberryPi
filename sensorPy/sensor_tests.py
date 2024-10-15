import unittest
from unittest.mock import patch
from MeassurementTypes import Temperature, RelativeHumidity, Pressure, MeasurementUnitType

class TestTemperature(unittest.TestCase):
    def setUp(self):
        self.temp = Temperature()

    def test_convert_value_to_celsius(self):
        self.temp.setValue(25)
        value, unit = self.temp.convert_value(self.temp.value, MeasurementUnitType.Celsius)
        self.assertEqual(value, 25)
        self.assertEqual(unit, MeasurementUnitType.Celsius)

    def test_convert_value_to_fahrenheit(self):
        self.temp.setValue(25)
        value, unit = self.temp.convert_value(self.temp.value, MeasurementUnitType.Fahrenheit)
        self.assertAlmostEqual(value, 77.0, places=1)
        self.assertEqual(unit, MeasurementUnitType.Fahrenheit)

    def test_convert_value_to_kelvin(self):
        self.temp.setValue(25)
        value, unit = self.temp.convert_value(self.temp.value, MeasurementUnitType.Kelvin)
        self.assertAlmostEqual(value, 298.15, places=2)
        self.assertEqual(unit, MeasurementUnitType.Kelvin)

    @patch('builtins.print')
    def test_print_temperature(self, mock_print):
        self.temp.setValue(25)
        self.temp.printValue()
        mock_print.assert_called_with('38;5;208Temperature : 025 38;5;208[°C]0')

class TestRelativeHumidity(unittest.TestCase):
    def setUp(self):
        self.rh = RelativeHumidity()

    def test_convert_value_to_percent(self):
        self.rh.setValue(50)
        value, unit = self.rh.convert_value(self.rh.value, MeasurementUnitType.Percent)
        self.assertEqual(value, 50)
        self.assertEqual(unit, MeasurementUnitType.Percent)

    @patch('builtins.print')
    def test_print_relative_humidity(self, mock_print):
        self.rh.setValue(50)
        self.rh.printValue()
        mock_print.assert_called_with("Relative Humidity: 50 %")

class TestPressure(unittest.TestCase):
    def setUp(self):
        self.pressure = Pressure()

    def test_convert_value_to_hectopascal(self):
        self.pressure.setValue(1013.25)
        value, unit = self.pressure.convert_value(self.pressure.value, MeasurementUnitType.Hectopascal)
        self.assertEqual(value, 1013.25)
        self.assertEqual(unit, MeasurementUnitType.Hectopascal)

    def test_convert_value_to_pascal(self):
        self.pressure.setValue(1013.25)
        value, unit = self.pressure.convert_value(self.pressure.value, MeasurementUnitType.Pascal)
        self.assertEqual(value, 101325)
        self.assertEqual(unit, MeasurementUnitType.Pascal)

    def test_convert_value_to_millimeter_of_mercury(self):
        self.pressure.setValue(1013.25)
        value, unit = self.pressure.convert_value(self.pressure.value, MeasurementUnitType.MillimeterOfMercury)
        self.assertAlmostEqual(value, 760.0, places=1)
        self.assertEqual(unit, MeasurementUnitType.MillimeterOfMercury)

    def test_convert_value_to_inch_of_mercury(self):
        self.pressure.setValue(1013.25)
        value, unit = self.pressure.convert_value(self.pressure.value, MeasurementUnitType.InchOfMercury)
        self.assertAlmostEqual(value, 29.92, places=2)
        self.assertEqual(unit, MeasurementUnitType.InchOfMercury)

    def test_convert_value_to_bar(self):
        self.pressure.setValue(1013.25)
        value, unit = self.pressure.convert_value(self.pressure.value, MeasurementUnitType.Bar)
        self.assertAlmostEqual(value, 1.01325, places=5)
        self.assertEqual(unit, MeasurementUnitType.Bar)

    def test_convert_value_to_atmosphere(self):
        self.pressure.setValue(1013.25)
        value, unit = self.pressure.convert_value(self.pressure.value, MeasurementUnitType.Atmosphere)
        self.assertAlmostEqual(value, 1.0, places=2)
        self.assertEqual(unit, MeasurementUnitType.Atmosphere)

    @patch('builtins.print')
    def test_print_pressure(self, mock_print):
        self.pressure.setValue(1013.25)
        self.pressure.printValue()
        mock_print.assert_called_with("Pressure: 1013.25 hPa")

if __name__ == '__main__':
    unittest.main()