"""Prints all times of the day that are palindromic in the format HH:MM:SS."""

from dataclasses import dataclass


@dataclass
class Time:
    hour: int
    minute: int
    second: int

    def __str__(self):
        return f"{self.hour}:{self.minute:02}:{self.second:02}"

    def is_palindrome(self):
        time_str = str(self).replace(":", "")
        return time_str == time_str[::-1]


def get_times():
    for hour in range(24):
        for minute in range(60):
            for second in range(60):
                yield Time(hour, minute, second)


def find_palindromic_times():
    for time in get_times():
        if time.is_palindrome():
            print(time)


if __name__ == "__main__":
    find_palindromic_times()
