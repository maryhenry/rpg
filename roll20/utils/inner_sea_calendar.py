import math
import sys

# Calendar Constants
MONTH_DAYS = [ 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31 ]
LEAP_DAYS = [ 31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31 ]
YEAR_LENGTH = sum(MONTH_DAYS)
LEAP_YEAR = 8
MOON_PERIOD = 29.5

WEEK = [ "Moonday", "Toilday", "Wealday", "Oathday", "Fireday", "Starday", "Sunday" ]

MONTH = [ "Abadius", "Calistril", "Pharast", "Gozren", "Desnus", "Sarenith", "Erastus", "Arodus", "Rova", "Lamashan", "Neth", "Kuthona" ]

MOON_PHASES = [ "Full Moon", "Waning Gibbous", "Third Quarter", "Waning Crescent", "New Moon", "Waxing Crescent", "First Quarter", "Waxing Gibbous" ]
PHASE_LENGTH = [ 3, 4, 4, 4, 2, 4, 4, 4 ]
BRIGHTNESS = [ 3, 2, 2, 1, 0, 1, 2, 2 ]

def getYear(epocDay):
    yearLength = (YEAR_LENGTH + ( 1.0 / LEAP_YEAR))

    year = math.ceil(epocDay / yearLength)

    return int(year);

def getDayInYear(epocDay):
    year = getYear(epocDay)

    yearLength = (YEAR_LENGTH + ( 1.0 / LEAP_YEAR))
    dayInYear = int(epocDay - (year-1) * yearLength) + 1

    return dayInYear;

def getMonthInYear(epocDay):
    cal = MONTH_DAYS
    isLeapYear = (getYear(epocDay) % 8) == 0
    if (isLeapYear):
        cal = LEAP_DAYS

    dayInYear = getDayInYear(epocDay)

    month = 0
    while dayInYear > cal[month]:
        dayInYear -= cal[month]
        month += 1

    return month + 1

def getDayInMonth(epocDay):
    cal = MONTH_DAYS
    isLeapYear = (getYear(epocDay) % 8) == 0
    if (isLeapYear):
        cal = LEAP_DAYS

    dayInYear = getDayInYear(epocDay)

    month = 0
    while dayInYear > cal[month]:
        dayInYear -= cal[month]
        month += 1

    return dayInYear


# Get the epoc day from a date. This is the number of days since the first
# day of the year in 1 AR. 1/1/1 is epoc day 1 (epoc day 0 does not exist).
def getEpocDay(day, month, year):
    cal = MONTH_DAYS
    isLeapYear = (year % 8) == 0
    if (isLeapYear):
        cal = LEAP_DAYS

    epocDay = (YEAR_LENGTH + ( 1.0 / LEAP_YEAR)) * (year - 1)
    epocDay += sum(cal[:month-1])
    epocDay += day

    return int(epocDay);

# Returns a number from 1 - 7.
def getDayOfWeek(day, month, year):
    epocDay = getEpocDay(day, month, year)
    dayOfWeek = (epocDay - 1) % len(WEEK) + 1

    return dayOfWeek

def getEpocDayOfWeek(epocDay):
    return (epocDay - 1) % len(WEEK) + 1

# Returns the name of the day for this date.
def getNamedDayOfWeek(day, month, year):
    dayOfWeek = getDayOfWeek(day, month, year)

    return WEEK[dayOfWeek - 1]

# Returns a number from 1 - 29.
def getMoonPhase(day, month, year):
    epocDay = getEpocDay(day, month, year)

    moonDay = epocDay - int(MOON_PERIOD * int(epocDay / MOON_PERIOD))
    phase = 0
    while (moonDay > 0):
        moonDay -= PHASE_LENGTH[phase]
        if (moonDay > 0):
            phase += 1

    return MOON_PHASES[phase]

def calendar(month, year):
    cal = MONTH_DAYS
    isLeapYear = (year % 8) == 0
    if (isLeapYear):
        cal = LEAP_DAYS

    epocStartDay = getEpocDay(1, month, year)
    epocEndDay = getEpocDay(cal[month-1], month, year)

    html = "<h2>" + MONTH[month - 1] + "</h2>\n"
    html += "<table>\n"

    html += "<tr>\n"
    for name in WEEK:
        html += "<th>" + name + "</th>\n"
    html += "</tr>\n"

    today = epocStartDay + 1 - getEpocDayOfWeek(epocStartDay)
    while today <= epocEndDay:
        if getEpocDayOfWeek(today) == 1:
            html += "<tr>\n"

        if today < epocStartDay:
            html += "<td></td>\n"
        else:
            html += "<td>" + str(getDayInMonth(today)) + "</td>\n"

        if getEpocDayOfWeek(today) == 7:
            html += "</tr>\n"

        today += 1

    html += "</table>"

    return html


if (len(sys.argv) == 4):
    argDay = int(sys.argv[3])
    argMonth = int(sys.argv[2])
    argYear = int(sys.argv[1])

    print getNamedDayOfWeek(argDay, argMonth, argYear) + " - " + getMoonPhase(argDay, argMonth, argYear)
elif (len(sys.argv) == 3):
    argMonth = int(sys.argv[2])
    argYear = int(sys.argv[1])

    print calendar(argMonth, argYear)
elif (len(sys.argv) == 2):
    argYear = int(sys.argv[1])

    print "<html>\n<head>\n<title>" + str(argYear) + " AR</title>\n</head>\n<body>\n"
    print "<style>td { width: 100px; height: 100px; border: 1px solid black; text-align: left; vertical-align: top; }</style>\n"

    print "<h1>" + str(argYear) + " AR</h1>\n"

    for month in range(1, 13):
        print calendar(month, argYear)
    print "</body>\n</html>\n"