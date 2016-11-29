eaters = dict()

with open("a") as f:
    for i, r in enumerate(f):
        if not r.startswith("phil"):
            continue
        try:
            stuff, number, action = r.strip().split()
        except ValueError:
            print "...", r
            continue
        if action == "EATING":
            if eaters[number] > 0:
                print ("ERROR: %s already eating!" % number)
            else:
                eaters[number] = 1
        if action == "THINKING":
            try:
                eaters[number] -= 1
            except KeyError:
                eaters[number] = 0

        ee = [e[0] for e in eaters.items() if e[1] > 0]
        if (len(ee) > 2):
                print ("ERROR: %d eating (%s), row %d" % (
                len(ee), str(ee), i))
