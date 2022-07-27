
import re

data = 'www.example.com'

print(re.findall(r'^(?!([^\.:]+\.)*example\.com:)', data))