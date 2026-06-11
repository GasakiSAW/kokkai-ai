from analysis.estat import get_time_series

data = get_time_series(
    "0000010206"
)

for row in data:
    print(row)
