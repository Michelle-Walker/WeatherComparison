class WeatherInfo:
    def __init__(self, temp, feels_like, temp_min, temp_max, pressure, humidity, **kwargs):
        self.temp = get_f_temp(temp)
        self.feels_like = get_f_temp(feels_like)
        self.temp_min = get_f_temp(temp_min)
        self.temp_max = get_f_temp(temp_max)
        self.pressure = pressure
        self.humidity = humidity
        self.description = None


def get_f_temp(K_temp):  # converts from K to deg F
    k_temp = K_temp
    f_temp = round((k_temp-273.15)*(9/5)+32, 1)
    return f_temp
