
import cenos_py
case = cenos_py.CenosCaseIH()
case.open("C:/path/to/case")

temperature = case.results.get_temperature(time="last")

average = temperature.average()
minimum = temperature.minimum()
maximum = temperature.maximum()
standard_deviation = temperature.standard_deviation()
max_deviation = abs(temperature - average).maximum()

print("Billet temperature uniformity")
print(f"Average temperature:       {average:.1f} °C")
print(f"Minimum temperature:       {minimum:.1f} °C")
print(f"Maximum temperature:       {maximum:.1f} °C")
print(f"Temperature spread:        {maximum - minimum:.1f} °C")
print(f"Standard deviation:        {standard_deviation:.1f} °C")
print(f"Maximum deviation from avg:{max_deviation:.1f} °C")

# shows the temperature field on the geometry
temperature.plot()
