"""
CS 196 FA18 HW4 Solutions
Andrew Park
"""

from collections import Counter

"""
most_common_char

Given an input string s, return the most common character in s.
"""
def most_common_char(s):
	v = Counter(s)
	return v.most_common()[0][0]


"""
alphabet_finder

Given an input string s, return the shortest prefix of s (i.e. some s' = s[0:i] for some 0 < i <= n)
that contains all the letters of the alphabet.
If there is no such prefix, return None.
Your function should recognize letters in both cases, i.e. "qwertyuiopASDFGHJKLzxcvbnm" is a valid alphabet.

Example 1:
	Argument:
		"qwertyuiopASDFGHJKLzxcvbnm insensitive paella"
	Return:
		"qwertyuiopASDFGHJKLzxcvbnm"

Example 2:
	Argument:
		"aardvarks are cool!"
	Return:
		None
"""
def alphabet_finder(s):
	letterLocations = {}
	
	for i, c in enumerate(s.lower()):
		if c not in 'qwertyuiopasdfghjklzxcvbnm':
			continue  # we don't care about anything but letters
		if c in letterLocations:
			continue
		letterLocations[c] = i
	
	if len(letterLocations) < 26:
		return None
	
	# we want the last letter that appears, hence the +1...
	return s[:max(letterLocations.values())+1]


"""
longest_unique_subarray

Given an input list of integers arr,
return a list with two values [a,b] such that arr[a:a+b] is the longest unique subarray.
That is to say, all the elements of arr[a:a+b] must be unique,
and b must be the largest value possible for the array.
If multiple such subarrays exist (i.e. same b, different a), use the lowest value of a.

Example:
	Argument:
		[1, 2, 3, 1, 4, 5, 6]
	Return:
		[1, 6]
"""
def longest_unique_subarray(arr):
	bestIndex = bestLength = start = 0
	running = {}

	for i, v in enumerate(arr):
		if v in running:
			start = max(start, running[v] + 1)
			# e.g. ABCBA
		
		running[v] = i
		
		if (i - start + 1) > bestLength: # winner?
			bestIndex = start
			bestLength = i - start + 1

	return [bestIndex, bestLength]


"""
string_my_one_true_love

A former(?) CA for this course really like[d] strings that have the same occurrences of letters.
This means the staff member likes "aabbcc", "ccddee", "abcabcabc", etcetera.

But the person who wrote all of your homework sets wants to trick the staff with really long strings,
that either could be the type of string that the staff member likes,
or a string that the CA would like if you remove exactly one character from the string.

Return True if it's a string that the homework creator made, and False otherwise.
Don't treat any characters specially, i.e. 'a' and 'A' are different characters.

Ungraded food for thought:
Ideally, your method should also work on integer arrays without any modification.

Example 1:
	Argument:
		"abcbabcdcdda"
		There are 3 a's, 3 b's, 3 c's, and 3 d's. That means it is a very likable string!
	Return:
		True

Example 2:
	Argument:
		"aaabbbcccddde"
		There are 3 a's, 3 b's, 3 c's, and 3 d's. We have 1 e, which we can remove.
	Return:
		True

Example 3:
	Argument:
		"aaabbbcccdddeeffgg"
		This string is similar to the other ones, except with 2 e's, f's and g's at the end.
		To make this string likable, we need to remove the 2 e's, f's, and g's or we can remove
		one a, b, c, and d. However all of these require more than one removal, so it becomes invalid.
	Return:
		False
"""
def string_my_one_true_love(s):
	count = Counter(s)
	vals = Counter(count.values())

	if (len(vals) == 1):  # everything appears the same amount of times
		return True
	if (len(vals) > 2):  # too many frequencies
		return False
	'''
	now we have two frequencies
	the second frequency must be either 1, or other frequency is plus 1
	thus you cann remove one unique char for equal freq among the remaining
	this is also broken
	'''
	mostCommonFreq = vals.most_common()[0]
	otherFreq = vals.most_common()[1]

	if (otherFreq[1] > 1):  # we can only remove 1
		return False
	# remove 1 from the other frequency doesn't equal most common frequency
	if (otherFreq[0] != 1 and otherFreq[0] != (mostCommonFreq[0] + 1)):
		return False
	
	return True


"""
alive_people

You are given a 2-dimensional list data. Each element in data is a list [birth_year, age_of_death].
Assume that the person was alive in the year (birth_year + age_of_death).
Given that data, return the year where the most people represented in the list were alive.
If there are multiple such years, return the earliest year.

Example:
	Argument:
		[[1920, 80], [1940, 22], [1961, 10]]
	Return:
		1961
"""
def alive_people(people):
	'''
	Let n = len(people), and k = the range of years when people are alive.
	This algorithm runs in O(n log n) time and O(n) space.
	Most O(n) time algorithms I've seen are O(k) space because they
	allocate memory for every year between birth and death dates,
	which is clearly not necessary.
	This is also the #2 cause of memory errors on this HW.
	If you use radix sort it's probably O(n log k), but at that point
	the time and space analysis gets really complicated.
	'''
	people = preprocess(people)

	pairs = list(people.items())
	pairs.sort()

	(bestYear, bestPeople) = (-float('inf'), -1)
	runningTotal = 0
	for i in pairs:
		runningTotal += i[1]  # net people influx
		# we don't need to check for year because this goes from earliest year
		# to latest possible year
		if (runningTotal > bestPeople):
			(bestYear, bestPeople) = (i[0], runningTotal)

	return bestYear


def preprocess(people):
	'''Converts people's birth age and lifetime into a log of events.
	+x means that x people came into existence
	-x means that x people are no longer living as of this year.
	Output is not sorted, because dictionary iteration order isn't dependable...
	'''
	result = {}
	for p in people:
		birth = p[0]
		death = birth + p[1] + 1
		# default insanity
		result[birth] = result.get(birth, 0) + 1
		result[death] = result.get(death, 0) - 1

	return result

"""
three_sum

Given an input list of integers arr, and a constant target t,
is there a triplet of distinct elements [a,b,c] so that a + b + c = t?

Return a 2-dimensional list of all the unique triplets as defined above.
Each inner list should be a triplet as we defined above.
We don't care about the order of triplets, nor the order of elements in each triplet.

Example:
	Arguments:
		[-1, 0, 1, 2, -1, -4], 0
	Return:
		[
			[-1, 0, 1],
			[-1, -1, 2]
		]
"""
def three_sum(arr, t):
	target = t
	'''
	this implementation is a translation of some pseudocode from Wikipedia.
	Unfortunately my implementation is broken.
	This problem was the #1 culprit of memory errors
	becaise naive solutions are O(n^3) memory.
	Now imagine what happens with len(arr) = 1000.
	'''
	arr = sorted(arr)  # O(n log(n))

	result = {}
	
	for i in range(len(arr) - 3):
		floor = arr[i]  # this limits the search scope
		(start, end) = (i + 1, len(arr) - 1)  # left and right bounds

		if (floor > target):
			break  # all the elements after floor are going to be too high

		while (start < end):
			(left, right) = (arr[start], arr[end])

			if (floor + left + right == target):  # perfect!
				if tuple([floor, left, right]) not in result:
					result[tuple([floor, left, right])] = [i, start, end]
			if (floor + left + right >= target):  # too high
				end -= 1
			else:  # too low
				start += 1

	return [list(a) for a in result.keys()]


"""
happy_numbers

Given an input integer n > 0, return the number of happy integers between 1 and n, bounds inclusive.
https://en.wikipedia.org/wiki/Happy_number

Example 1:
	Argument:
		8
		The happy numbers between 1 and 8 are 1 and 7 (7 -> 49 -> 97 -> 130 -> 10 -> 1)
	Return:
		2468 // 1234 (i.e., 2)
Example 2:
	Argument:
		15
	Return:
		4294967296 ** (1 / 16) (i.e., 4)
"""
def happy_numbers(n):
	"""This code is not optimized well but it passes all test cases."""
	happys = 0
	alreadyNotHappy = []
	
	for i in range(1, n+1):
		if Counter(str(i)) in alreadyNotHappy:
			continue
		if is_happy(i):
			happys += 1
		else:
			alreadyNotHappy.append(Counter(str(i)))
	
	return happys


def is_happy(n):
	"""Given an integer input, returns if the number is happy or not.
	This is surprisingly efficient, because for a given number with d digits,
	the sum of digits squared is at most 81d."""
	notHappy = set([4, 16, 37, 58, 89, 145, 42, 20])  # from Wikipedia
	
	while n not in notHappy and n != 1:
		n = digits_squared(n)
	
	if n in notHappy:
		return False
	
	return True


def digits_squared(n):
	"""Given an integer input, returns the sum of its digits squared."""
	digitCount = Counter(str(n))
	# this is guaranteed to be digits now
	# also this counts for my dictionary use
	
	summ = 0
	for d in digitCount:
		summ += (int(d) ** 2) * digitCount[d]
		# doing a zero check here wouldn't save much time, so we don't bother
	
	return summ


"""
zero_sum_subarray

Given an input list of integers arr,
return a list with two values [a,b] such that sum(arr[a:a+b]) == 0.
In plain English, give us the location of a subarray of arr that starts at index a
and continues for b elements, so that the sum of the subarray you indicated is zero.
If multiple such subarrays exist, use the lowest valid a, and then lowest valid b,
in that order of priority.
If no such subarray exists, return None.

Ungraded food for thought:
Think about how to generalize your solution to any arbitrary target sum.

Example 1:
	Argument:
		[0, 1, 2, 3, 4, 5]
		Clearly, the first element by itself forms a subarray with sum == 0.
	Return:
		[0, 1]

Example 2:
	Argument:
		[10, 20, -20, 3, 21, 2, -6]
		In this case, arr[1:3] = [20, -20], so there is a zero sum subarray.
	Return:
		[1, 2]
"""
def zero_sum_subarray(arr):
	d = {}
	partialsum = 0
	for i, v in enumerate(arr):
		
		partialsum += v
		
		if v == 0: # obvious case
			return [i, 1]
		
		if (partialsum == 0): # sum(arr[0:v+1]) == 0
			return [0, i + 1]
		
		'''
		if a given partial sum appears TWICE, this implies the slice between
		the two occurrences of the value then has partial sum zero
		'''
		if (partialsum in d):
			return [d[partialsum] + 1, i - d[partialsum]]
		
		d[partialsum] = i
	
	return None



