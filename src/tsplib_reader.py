def read_tsplib(filepath):
    cities = []
    reading_coords = False

    with open(filepath, "r") as f:
        for line in f:
            line = line.strip()

            if line == "NODE_COORD_SECTION":
                reading_coords = True
                continue

            if line == "EOF":
                break

            if reading_coords:
                parts = line.split()
                # formato: id x y
                x = float(parts[1])
                y = float(parts[2])
                cities.append((x, y))

    return cities
