import datetime

from approvaltests import verify_all, Options, verify_as_json, verify
from approvaltests.scrubbers.date_scrubbers import scrub_all_dates, create_regex_scrubber


def test_full_stack_scrubbing():
    verify_all(
        "expanding twos",
        [1, 2, 12, 21, 121, 131, 222],
        options=Options().with_scrubber(lambda t: t.replace("2", "two")),
    )


def test_date_scrubbing():
    date1 = str(datetime.datetime(year=2000, month=1, day=2))
    date2 = str(datetime.datetime(year=2000, month=1, day=3))
    date3 = str(datetime.datetime(year=2000, month=1, day=4))
    mydict = {"start": date1, "pause": date2, "resume": date2, "end": date3}
    verify_as_json(mydict, options=Options().with_scrubber(scrub_all_dates))

def test_regex():
    verify('and then jane said "blah blah blah "', options=Options().with_scrubber(create_regex_scrubber("(blah )+", "[nonsense]")))


# TODO
# def template_regex_scrubber():
#     return create_regex_scrubber("(blah )*", lambda n: "[nonsense]")
#
#
# def test_guid():
#     pass
#
# def test_combine_scrubbers():
#     verify("blah1 date guid", options=Options().with_scrubber(combine_scrubbers('guid, date, nonsense')))
#
# def test_date_finder_scrubbers():
#     pass