# from pyowm import OWM
# import json
# import pprint

# owm  = OWM('e6378ca5eccf071ead2565ccff059357')
# mgr = owm.weather_manager()
# one_call = mgr.one_call(lat=28.5355, lon=77.3390)
# curr_data = json.dumps(one_call.current.__dict__)
# pprint(curr_data)

from pyowm import OWM
import json
import pprint

owm = OWM('0f8b321c68552dff33eeb5625f971c39')
mgr = owm.weather_manager()
one_call = mgr.one_call(lat=28.5355, lon=77.3910)
current_data = json.dumps(one_call.current.__dict__)
print(current_data)