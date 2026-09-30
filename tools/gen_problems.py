#!/usr/bin/env python3
"""Generates backend/src/db/seed.sql.
Every expected output is computed by a reference solution in this file, so tests are
guaranteed consistent. Run:  python tools/gen_problems.py
"""
import os, re, json, math, heapq, random, string, bisect
from collections import Counter, deque

R = random.Random(2026)
BIG = 15000
P = []

def slugify(t): return re.sub(r'[^a-z0-9]+', '-', t.lower()).strip('-')
def D(text, inp, out):
    return (text.strip() + "\n\n**Input**\n" + "\n".join("- " + x for x in inp)
            + "\n\n**Output**\n" + "\n".join("- " + x for x in out))
def add(title, diff, desc, solve, tests):
    P.append(dict(title=title, slug=slugify(title), diff=diff, desc=desc, solve=solve, tests=tests))
def ints(s): return list(map(int, s.split()))
def ri(lo, hi, n): return [R.randint(lo, hi) for _ in range(n)]
def A(arr): return f"{len(arr)}\n{' '.join(map(str, arr))}\n"
def rs(alpha, n): return ''.join(R.choice(alpha) for _ in range(n))
L = string.ascii_lowercase

# ------------------------------------------------------------------ EASY (20)
add("Sum of Array", "easy",
    D("Read `n`, then `n` integers. Print their sum.",
      ["Line 1: `n` (1 ≤ n ≤ 100000)", "Line 2: `n` space-separated integers"],
      ["A single integer: the sum. It can exceed 32 bits."]),
    lambda s: str(sum(ints(s)[1:])),
    [A([1, 2, 3]), A([-5]), A([10, 20, 30, 40, 50]), A([10**9] * 4), A(ri(-10**9, 10**9, 5000))])

add("Reverse the Words", "easy",
    D("Read one line of words separated by single spaces. Print the words in reverse order, separated by single spaces.",
      ["One line with 1 to 1000 words."], ["The same words in reverse order."]),
    lambda s: ' '.join(reversed(s.split())),
    ["hello world\n", "a b c d\n", "single\n", "the quick brown fox\n",
     ' '.join(rs(L, R.randint(1, 8)) for _ in range(500)) + "\n"])

add("Maximum of Array", "easy",
    D("Read `n` integers and print the largest one.",
      ["Line 1: `n` (1 ≤ n ≤ 100000)", "Line 2: `n` integers"], ["The maximum value."]),
    lambda s: str(max(ints(s)[1:])),
    [A([3, 1, 2]), A([-7]), A([-5, -2, -9]), A([5, 5, 5]), A(ri(-10**9, 10**9, 1000))])

add("Count Vowels", "easy",
    D("Count the vowels (`a e i o u`, in either case) in one line of text.",
      ["One line of up to 1000 characters."], ["The number of vowels."]),
    lambda s: str(sum(c in 'aeiouAEIOU' for c in s.rstrip('\n'))),
    ["Hello World\n", "xyz\n", "AEIOUaeiou\n", "Competitive Programming is fun\n", "rhythm\n"])

_half = rs(L, 500)
add("Palindrome Check", "easy",
    D("Decide whether a word reads the same forwards and backwards.",
      ["One lowercase word, 1 to 5000 letters."], ["`YES` if it is a palindrome, otherwise `NO`."]),
    lambda s: "YES" if s.strip() == s.strip()[::-1] else "NO",
    ["racecar\n", "hello\n", "a\n", "abba\n", "abca\n", _half + _half[::-1] + "\n", _half + "x" + _half[::-1][:-1] + "y\n"])

def fizz(s):
    out = []
    for i in range(1, int(s) + 1):
        out.append("FizzBuzz" if i % 15 == 0 else "Fizz" if i % 3 == 0 else "Buzz" if i % 5 == 0 else str(i))
    return "\n".join(out)
add("FizzBuzz", "easy",
    D("Print the numbers from 1 to `n`, one per line. For multiples of 3 print `Fizz`, for multiples of 5 print `Buzz`, and for multiples of both print `FizzBuzz`.",
      ["A single integer `n` (1 ≤ n ≤ 10000)"], ["`n` lines."]),
    fizz, ["15\n", "1\n", "3\n", "5\n", "30\n", "100\n"])

add("Factorial", "easy",
    D("Compute `n!` (the product of 1 through n; `0! = 1`).",
      ["A single integer `n` (0 ≤ n ≤ 20)"], ["`n!`. It fits in a signed 64-bit integer."]),
    lambda s: str(math.factorial(int(s))), ["5\n", "0\n", "1\n", "10\n", "20\n"])

add("Even and Odd Count", "easy",
    D("Count how many numbers in a list are even and how many are odd.",
      ["Line 1: `n` (1 ≤ n ≤ 100000)", "Line 2: `n` integers (may be negative)"],
      ["Two integers separated by a space: the even count, then the odd count."]),
    lambda s: (lambda a: f"{sum(x % 2 == 0 for x in a)} {sum(x % 2 != 0 for x in a)}")(ints(s)[1:]),
    [A([1, 2, 3, 4, 5]), A([-3, -2, -1, 0]), A([2, 4, 6]), A([7]), A(ri(-10**6, 10**6, 2000))])

def fib(n):
    a, b = 0, 1
    for _ in range(n): a, b = b, a + b
    return a
add("Fibonacci Number", "easy",
    D("The Fibonacci sequence starts `F(0) = 0`, `F(1) = 1`, and each next term is the sum of the previous two. Print `F(n)`.",
      ["A single integer `n` (0 ≤ n ≤ 90)"], ["`F(n)`. It fits in a signed 64-bit integer."]),
    lambda s: str(fib(int(s))), ["0\n", "1\n", "10\n", "50\n", "90\n"])

def is_prime(n):
    if n < 2: return False
    i = 2
    while i * i <= n:
        if n % i == 0: return False
        i += 1
    return True
add("Prime Check", "easy",
    D("Decide whether `n` is a prime number.",
      ["A single integer `n` (1 ≤ n ≤ 10^12)"], ["`YES` if `n` is prime, otherwise `NO`."]),
    lambda s: "YES" if is_prime(int(s)) else "NO",
    ["1\n", "2\n", "17\n", "100\n", "999999937\n", "999999999989\n", "999999999991\n"])

add("Digit Sum", "easy",
    D("Add up the decimal digits of `n`.", ["A single integer `n` (0 ≤ n ≤ 10^18)"], ["The sum of its digits."]),
    lambda s: str(sum(map(int, str(int(s))))),
    ["12345\n", "0\n", "999999999999999999\n", "100\n", "987654321\n"])

add("Greatest Common Divisor", "easy",
    D("Find the greatest common divisor of two positive integers.",
      ["Two integers `a` and `b` (1 ≤ a, b ≤ 10^18) on one line"], ["`gcd(a, b)`"]),
    lambda s: str(math.gcd(*ints(s))),
    ["12 18\n", "17 5\n", "1000000000000 250000000000\n", "1 1\n", "48 180\n", "999999999999999989 999999999999999967\n"])

add("Count Words", "easy",
    D("Count the words in a line. Words are separated by one or more spaces, and the line may start or end with spaces.",
      ["One line of up to 10000 characters."], ["The number of words."]),
    lambda s: str(len(s.split())),
    ["hello world\n", "  spaced   out  words \n", "one\n", "a b c d e f g\n", ' '.join(rs(L, 4) for _ in range(300)) + "\n"])

add("Array Range", "easy",
    D("Print the difference between the largest and smallest numbers in a list.",
      ["Line 1: `n` (1 ≤ n ≤ 100000)", "Line 2: `n` integers"], ["`max - min`"]),
    lambda s: (lambda a: str(max(a) - min(a)))(ints(s)[1:]),
    [A([3, 9, 1, 4]), A([7]), A([-10, 10]), A([5, 5, 5, 5]), A(ri(-10**9, 10**9, 1000))])

add("Reverse String", "easy",
    D("Print a line of text reversed.", ["One line (no leading or trailing spaces), up to 1000 characters."], ["The reversed line."]),
    lambda s: s.rstrip('\n')[::-1],
    ["hello\n", "a\n", "racecar\n", "Code Arena\n", "abc def ghi\n"])

add("Leap Year", "easy",
    D("A year is a leap year if it is divisible by 4, except years divisible by 100 that are not divisible by 400.",
      ["A single integer `year` (1 ≤ year ≤ 9999)"], ["`YES` if it is a leap year, otherwise `NO`."]),
    lambda s: "YES" if (int(s) % 4 == 0 and (int(s) % 100 != 0 or int(s) % 400 == 0)) else "NO",
    ["2000\n", "1900\n", "2024\n", "2023\n", "2100\n", "1600\n"])

add("Power of Two", "easy",
    D("Decide whether `n` equals `2^k` for some integer `k ≥ 0`.",
      ["A single integer `n` (1 ≤ n ≤ 10^18)"], ["`YES` or `NO`."]),
    lambda s: "YES" if (int(s) & (int(s) - 1)) == 0 else "NO",
    ["1\n", "2\n", "3\n", "1024\n", "1000\n", f"{2**59}\n", f"{2**59 + 1}\n"])

add("Count Character", "easy",
    D("Count how many times a character appears in a word.",
      ["Line 1: a word of lowercase letters (up to 100000 letters)", "Line 2: a single lowercase letter"], ["The number of occurrences."]),
    lambda s: (lambda w, c: str(w.count(c)))(*s.split()),
    ["hello\nl\n", "banana\na\n", "xyz\nq\n", "mississippi\ns\n", rs(L, 3000) + "\ne\n"])

add("Anagram Check", "easy",
    D("Two words are anagrams if one can be rearranged into the other using every letter exactly once.",
      ["Line 1: the first word", "Line 2: the second word (lowercase letters, up to 100000 each)"], ["`YES` or `NO`."]),
    lambda s: (lambda a, b: "YES" if sorted(a) == sorted(b) else "NO")(*s.split()),
    ["listen\nsilent\n", "hello\nworld\n", "a\na\n", "aab\nabb\n", "triangle\nintegral\n",
     (lambda w: w + "\n" + ''.join(R.sample(w, len(w))) + "\n")(rs(L, 4000)),
     (lambda w: w + "\n" + ''.join(R.sample(w, len(w)))[:-1] + ("a" if w[-1] != "a" else "b") + "\n")(rs(L, 4000))])

add("Remove Duplicates", "easy",
    D("Remove repeated numbers from a list, keeping only the first occurrence of each.",
      ["Line 1: `n` (1 ≤ n ≤ 100000)", "Line 2: `n` integers"], ["The remaining numbers in their original order, separated by spaces."]),
    lambda s: ' '.join(map(str, dict.fromkeys(ints(s)[1:]))),
    [A([1, 2, 2, 3, 1]), A([5, 5, 5]), A([9]), A([3, 1, 2]), A(ri(0, 500, 3000))])

# ---------------------------------------------------------------- MEDIUM (21)
def two_sum(s):
    t = ints(s); n = t[0]; a = t[1:1 + n]; tg = t[1 + n]
    seen, res = {}, []
    for i, x in enumerate(a):
        if tg - x in seen: res.append((seen[tg - x], i))
        seen[x] = i
    assert len(res) == 1, res
    return f"{res[0][0]} {res[0][1]}"
def two_sum_big(n):
    while True:
        a = R.sample(range(-10**9, 10**9), n)
        i, j = sorted(R.sample(range(n), 2)); tg = a[i] + a[j]
        S = set(a)
        if sum(1 for x in a if (tg - x) in S and x < tg - x) == 1:
            return f"{n}\n{' '.join(map(str, a))}\n{tg}\n"
add("Two Sum", "medium",
    D("Given `n` integers and a target, find the two different positions whose values add up to the target.",
      ["Line 1: `n` (2 ≤ n ≤ 100000)", "Line 2: `n` integers", "Line 3: the target"],
      ["The two 0-based indices, smaller first, separated by a space. Exactly one answer exists.",
       "Checking every pair is too slow for large inputs."]),
    two_sum,
    ["4\n2 7 11 15\n9\n", "3\n3 2 4\n6\n", "2\n3 3\n6\n", "5\n1 5 3 8 12\n20\n", "4\n-3 4 3 90\n0\n", two_sum_big(BIG)])

def valid_par(s):
    pair = {')': '(', ']': '[', '}': '{'}; st = []
    for c in s.strip():
        if c in '([{': st.append(c)
        else:
            if not st or st.pop() != pair[c]: return "NO"
    return "NO" if st else "YES"
def gen_balanced(pairs):
    out, st, opens = [], [], pairs
    for _ in range(2 * pairs):
        if opens > 0 and (not st or R.random() < 0.5):
            ch = R.choice('([{'); st.append(ch); out.append(ch); opens -= 1
        else:
            out.append({'(': ')', '[': ']', '{': '}'}[st.pop()])
    return ''.join(out)
_bal = gen_balanced(4000)
add("Valid Parentheses", "medium",
    D("A string of brackets `()[]{}` is valid if every bracket is closed by the same type, in the correct order.",
      ["One string of 1 to 20000 bracket characters."], ["`YES` if valid, otherwise `NO`."]),
    valid_par, ["()[]{}\n", "(]\n", "([{}])\n", "((\n", ")(\n", "{[()]}[\n", _bal + "\n", _bal + "(\n"])

def lcp(s):
    t = s.split(); n = int(t[0]); w = t[1:1 + n]; p = w[0]
    for x in w[1:]:
        while not x.startswith(p): p = p[:-1]
    return p if p else "NONE"
_pref = rs(L, 200)
add("Longest Common Prefix", "medium",
    D("Find the longest prefix shared by every word in a list.",
      ["Line 1: `n` (1 ≤ n ≤ 1000)", "Next `n` lines: one lowercase word each (up to 300 letters)"],
      ["The common prefix, or `NONE` if the words share no first letter."]),
    lcp, ["3\nflower\nflow\nflight\n", "3\ndog\nracecar\ncar\n", "4\ninterview\ninternet\ninternal\ninterval\n",
          "1\nalone\n", "3\nabc\nabc\nabc\n", "1000\n" + "\n".join(_pref + rs(L, R.randint(1, 50)) for _ in range(1000)) + "\n"])

def kadane(s):
    a = ints(s)[1:]; best = cur = a[0]
    for x in a[1:]:
        cur = max(x, cur + x); best = max(best, cur)
    return str(best)
add("Maximum Subarray Sum", "medium",
    D("Find the largest sum of any non-empty run of consecutive numbers.",
      ["Line 1: `n` (1 ≤ n ≤ 100000)", "Line 2: `n` integers between -10^4 and 10^4"], ["The largest possible sum."]),
    kadane, [A([-2, 1, -3, 4, -1, 2, 1, -5, 4]), A([-3, -1, -2]), A([5]), A([1, 2, 3, 4]), A(ri(-1000, 1000, BIG))])

def bsearch(s):
    t = ints(s); n = t[0]; a = t[1:1 + n]; m = t[1 + n]; q = t[2 + n:2 + n + m]
    pos = {x: i for i, x in enumerate(a)}
    return "\n".join(str(pos.get(x, -1)) for x in q)
def bs_in(a, q): return f"{len(a)}\n{' '.join(map(str, a))}\n{len(q)}\n{' '.join(map(str, q))}\n"
_bsa = sorted(R.sample(range(-10**7, 10**7), BIG))
add("Binary Search Queries", "medium",
    D("You are given a sorted list of distinct integers and several queries. For each query, find the position of the value in the list.",
      ["Line 1: `n` (1 ≤ n ≤ 100000)", "Line 2: `n` distinct integers in increasing order",
       "Line 3: `m` (1 ≤ m ≤ 100000)", "Line 4: `m` query values"],
      ["`m` lines: the 0-based index of each query value, or `-1` if it is not in the list."]),
    bsearch, [bs_in([1, 3, 5, 7, 9, 11], [7, 1, 11, 4, 12, 0]), bs_in([42], [42, 41]), bs_in([-5, 0, 5], [0, -5, 5, 6]),
              bs_in(_bsa, [R.choice(_bsa) if R.random() < 0.5 else R.randint(-10**7, 10**7) for _ in range(BIG)])])

def rotate(s):
    t = ints(s); n, k = t[0], t[1]; a = t[2:2 + n]; k %= n
    return ' '.join(map(str, a[-k:] + a[:-k] if k else a))
def rot_in(a, k): return f"{len(a)} {k}\n{' '.join(map(str, a))}\n"
add("Rotate Array", "medium",
    D("Rotate a list to the right by `k` positions. The last `k` elements move to the front.",
      ["Line 1: `n` and `k` (1 ≤ n ≤ 100000, 0 ≤ k ≤ 10^9)", "Line 2: `n` integers"], ["The rotated list, separated by spaces."]),
    rotate, [rot_in([1, 2, 3, 4, 5], 2), rot_in([7], 100), rot_in([1, 2, 3, 4], 0), rot_in([1, 2, 3, 4, 5, 6], 10**9),
             rot_in(ri(-999, 999, BIG), R.randint(1, 10**9))])

add("Pascal Triangle Row", "medium",
    D("Rows of Pascal's triangle start with row 0 = `1`. Each inner number is the sum of the two above it. Print row `n`.",
      ["A single integer `n` (0 ≤ n ≤ 30)"], ["The numbers of row `n`, separated by spaces."]),
    lambda s: ' '.join(str(math.comb(int(s), k)) for k in range(int(s) + 1)), ["0\n", "1\n", "4\n", "10\n", "30\n"])

def count_primes(n):
    if n < 2: return 0
    sv = bytearray([1]) * (n + 1); sv[0] = sv[1] = 0
    for i in range(2, int(n**0.5) + 1):
        if sv[i]: sv[i * i::i] = bytearray(len(sv[i * i::i]))
    return sum(sv)
add("Count Primes", "medium",
    D("Count the prime numbers that are less than or equal to `n`.",
      ["A single integer `n` (1 ≤ n ≤ 1000000)"], ["The number of primes up to `n`."]),
    lambda s: str(count_primes(int(s))), ["10\n", "1\n", "2\n", "100\n", "500000\n", "1000000\n"])

def stock(s):
    p = ints(s)[1:]; lo = p[0]; best = 0
    for x in p[1:]:
        best = max(best, x - lo); lo = min(lo, x)
    return str(best)
_p, _prices = 5000, []
for _ in range(BIG):
    _p = max(1, _p + R.randint(-50, 50)); _prices.append(_p)
add("Best Time to Buy and Sell", "medium",
    D("Given a list of daily prices, choose one day to buy and a later day to sell to maximize profit.",
      ["Line 1: `n` days (1 ≤ n ≤ 100000)", "Line 2: `n` prices (1 ≤ price ≤ 10^9)"], ["The maximum profit, or `0` if no profit is possible."]),
    stock, [A([7, 1, 5, 3, 6, 4]), A([7, 6, 4, 3, 1]), A([5]), A([1, 2]), A(_prices)])

def missing(s):
    t = ints(s); n = t[0]; return str(n * (n + 1) // 2 - sum(t[1:1 + n]))
_nums = list(range(BIG + 1)); _nums.remove(R.randint(0, BIG)); R.shuffle(_nums)
add("Missing Number", "medium",
    D("A list holds `n` distinct numbers taken from `0..n`, so exactly one number in that range is missing. Find it.",
      ["Line 1: `n` (1 ≤ n ≤ 100000)", "Line 2: `n` distinct integers"], ["The missing number."]),
    missing, [A([3, 0, 1]), A([0]), A([1]), A([9, 6, 4, 2, 3, 5, 7, 0, 1]), A(_nums)])

def merge_sorted(s):
    t = ints(s); n, m = t[0], t[1]; return ' '.join(map(str, sorted(t[2:2 + n] + t[2 + n:2 + n + m])))
def ms_in(a, b): return f"{len(a)} {len(b)}\n{' '.join(map(str, a))}\n{' '.join(map(str, b))}\n"
add("Merge Sorted Arrays", "medium",
    D("Merge two lists that are each sorted in increasing order into one sorted list.",
      ["Line 1: `n` and `m` (1 ≤ n, m ≤ 100000)", "Line 2: the first list", "Line 3: the second list"], ["The merged list, separated by spaces."]),
    merge_sorted, [ms_in([1, 3, 5], [2, 4, 6]), ms_in([1], [1]), ms_in([-5, 0, 10], [-6, -5, 11, 12]),
                   ms_in([1, 2, 3], [7, 8, 9]), ms_in(sorted(ri(-10**6, 10**6, 5000)), sorted(ri(-10**6, 10**6, 5000)))])

def most_freq(s):
    c = Counter(s.strip()); b = min(c, key=lambda x: (-c[x], x)); return f"{b} {c[b]}"
add("Most Frequent Character", "medium",
    D("Find the letter that appears most often in a word. If several letters tie, choose the one that comes first alphabetically.",
      ["One lowercase word of up to 100000 letters."], ["The letter and its count, separated by a space."]),
    most_freq, ["hello\n", "aabbcc\n", "z\n", "mississippi\n", rs(L, 5000) + "\n"])

def to_roman(n):
    out = ''
    for v, sym in [(1000, 'M'), (900, 'CM'), (500, 'D'), (400, 'CD'), (100, 'C'), (90, 'XC'), (50, 'L'), (40, 'XL'), (10, 'X'), (9, 'IX'), (5, 'V'), (4, 'IV'), (1, 'I')]:
        while n >= v: out += sym; n -= v
    return out
def from_roman(r):
    m = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}; tot = 0
    for i, c in enumerate(r):
        tot += -m[c] if i + 1 < len(r) and m[r[i + 1]] > m[c] else m[c]
    return tot
add("Roman to Integer", "medium",
    D("Convert a Roman numeral to a number. Symbols: `I=1 V=5 X=10 L=50 C=100 D=500 M=1000`. A smaller symbol before a larger one is subtracted (`IV = 4`, `IX = 9`, `XL = 40`, `XC = 90`, `CD = 400`, `CM = 900`).",
      ["One valid Roman numeral representing a value from 1 to 3999."], ["The integer value."]),
    lambda s: str(from_roman(s.strip())), [to_roman(x) + "\n" for x in [3, 58, 1994, 4, 3999, 9, 444, 2024]])

def spiral(s):
    t = ints(s); r, c = t[0], t[1]; g = [t[2 + i * c:2 + (i + 1) * c] for i in range(r)]
    res, top, bot, left, right = [], 0, r - 1, 0, c - 1
    while top <= bot and left <= right:
        res += g[top][left:right + 1]; top += 1
        for i in range(top, bot + 1): res.append(g[i][right])
        right -= 1
        if top <= bot:
            res += g[bot][left:right + 1][::-1]; bot -= 1
        if left <= right:
            for i in range(bot, top - 1, -1): res.append(g[i][left])
            left += 1
    return ' '.join(map(str, res))
def mat_in(g): return f"{len(g)} {len(g[0])}\n" + "\n".join(' '.join(map(str, row)) for row in g) + "\n"
add("Spiral Order", "medium",
    D("Read a grid of numbers and print its elements in clockwise spiral order, starting at the top-left corner.",
      ["Line 1: rows `r` and columns `c` (1 ≤ r, c ≤ 200)", "Next `r` lines: `c` integers each"], ["All `r × c` numbers in spiral order, separated by spaces."]),
    spiral, [mat_in([[1, 2, 3], [4, 5, 6], [7, 8, 9]]), mat_in([[1, 2, 3, 4]]), mat_in([[1], [2], [3], [4]]),
             mat_in([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]]), mat_in([ri(0, 99, 50) for _ in range(50)]), mat_in([ri(0, 99, 7) for _ in range(30)])])

def sub_k(s):
    t = ints(s); n, k = t[0], t[1]; a = t[2:2 + n]; cnt = Counter({0: 1}); pre = tot = 0
    for x in a:
        pre += x; tot += cnt[pre - k]; cnt[pre] += 1
    return str(tot)
def sk_in(a, k): return f"{len(a)} {k}\n{' '.join(map(str, a))}\n"
add("Subarray Sum Equals K", "medium",
    D("Count the runs of consecutive numbers (subarrays) whose sum is exactly `k`. Numbers may be negative or zero.",
      ["Line 1: `n` and `k` (1 ≤ n ≤ 100000, |k| ≤ 10^9)", "Line 2: `n` integers"], ["The number of subarrays with sum `k`."]),
    sub_k, [sk_in([1, 1, 1], 2), sk_in([1, 2, 3], 3), sk_in([0, 0, 0, 0], 0), sk_in([3, 4, 7, 2, -3, 1, 4, 2], 7), sk_in(ri(-5, 5, BIG), 7)])

def long_sub(s):
    s = s.strip(); last, start, best = {}, 0, 0
    for i, c in enumerate(s):
        if c in last and last[c] >= start: start = last[c] + 1
        last[c] = i; best = max(best, i - start + 1)
    return str(best)
add("Longest Unique Substring", "medium",
    D("Find the length of the longest stretch of consecutive characters in which no character repeats.",
      ["One string of letters and digits, 1 to 100000 characters."], ["The length of the longest such stretch."]),
    long_sub, ["abcabcbb\n", "bbbbb\n", "pwwkew\n", "a\n", "abcdefg\n", rs(string.ascii_letters + string.digits, BIG) + "\n", rs("abcdefghij", BIG) + "\n"])

def coin(s):
    t = ints(s); n, amt = t[0], t[1]; coins = t[2:2 + n]; INF = 10**9; dp = [0] + [INF] * amt
    for a in range(1, amt + 1):
        for c in coins:
            if c <= a and dp[a - c] + 1 < dp[a]: dp[a] = dp[a - c] + 1
    return str(dp[amt] if dp[amt] < INF else -1)
def cc_in(c, a): return f"{len(c)} {a}\n{' '.join(map(str, c))}\n"
add("Coin Change", "medium",
    D("You have unlimited coins of each given value. Find the fewest coins needed to make an exact amount.",
      ["Line 1: number of coin types `n` (1 ≤ n ≤ 50) and the amount (0 ≤ amount ≤ 10000)", "Line 2: the `n` coin values"],
      ["The minimum number of coins, or `-1` if the amount cannot be made."]),
    coin, [cc_in([1, 2, 5], 11), cc_in([2], 3), cc_in([1], 0), cc_in([186, 419, 83, 408], 6249), cc_in(R.sample(range(7, 400), 30), 10000)])

def climb(s):
    n = int(s)
    if n <= 2: return str(n)
    a, b = 1, 2
    for _ in range(n - 2): a, b = b, a + b
    return str(b)
add("Climbing Stairs", "medium",
    D("You climb a staircase of `n` steps, taking 1 or 2 steps at a time. Count the distinct ways to reach the top.",
      ["A single integer `n` (1 ≤ n ≤ 80)"], ["The number of ways. It fits in a signed 64-bit integer."]),
    climb, ["1\n", "2\n", "3\n", "10\n", "45\n", "80\n"])

def caesar(s):
    lines = s.split('\n'); k = int(lines[0]) % 26; out = []
    for c in lines[1]:
        if 'a' <= c <= 'z': out.append(chr((ord(c) - 97 + k) % 26 + 97))
        elif 'A' <= c <= 'Z': out.append(chr((ord(c) - 65 + k) % 26 + 65))
        else: out.append(c)
    return ''.join(out)
add("Caesar Cipher", "medium",
    D("Shift every letter forward through the alphabet by `k` places, wrapping from `z` to `a`. Keep upper and lower case, and leave other characters unchanged.",
      ["Line 1: `k` (0 ≤ k ≤ 1000)", "Line 2: the text (up to 1000 characters, no trailing spaces)"], ["The encrypted text."]),
    caesar, ["3\nHello, World!\n", "0\nabc\n", "13\nUryyb Jbeyq\n", "25\nZebra-Crossing 42\n", "1000\nThe Quick Brown Fox Jumps Over The Lazy Dog\n"])

def grid_in(rows): return f"{len(rows)} {len(rows[0])}\n" + "\n".join(rows) + "\n"
def rgrid(r, c, p, ch): return [''.join(ch[1] if R.random() < p else ch[0] for _ in range(c)) for _ in range(r)]
def islands(s):
    lines = s.split('\n'); r, c = map(int, lines[0].split()); g = lines[1:1 + r]
    seen = [[False] * c for _ in range(r)]; cnt = 0
    for i in range(r):
        for j in range(c):
            if g[i][j] == '1' and not seen[i][j]:
                cnt += 1; seen[i][j] = True; dq = deque([(i, j)])
                while dq:
                    x, y = dq.popleft()
                    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < r and 0 <= ny < c and g[nx][ny] == '1' and not seen[nx][ny]:
                            seen[nx][ny] = True; dq.append((nx, ny))
    return str(cnt)
add("Number of Islands", "medium",
    D("A grid of `1` (land) and `0` (water) is given. An island is a group of land cells connected up, down, left or right. Count the islands.",
      ["Line 1: rows `r` and columns `c` (1 ≤ r, c ≤ 300)", "Next `r` lines: a string of `c` characters, each `0` or `1`"], ["The number of islands."]),
    islands, [grid_in(["11110", "11010", "11000", "00000"]), grid_in(["11000", "11000", "00100", "00011"]), "1 1\n0\n", "1 1\n1\n",
              grid_in(rgrid(150, 150, 0.45, "01"))])

def grid_bfs(s):
    lines = s.split('\n'); r, c = map(int, lines[0].split()); g = lines[1:1 + r]
    dist = [[-1] * c for _ in range(r)]; dist[0][0] = 0; dq = deque([(0, 0)])
    while dq:
        x, y = dq.popleft()
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nx, ny = x + dx, y + dy
            if 0 <= nx < r and 0 <= ny < c and g[nx][ny] == '.' and dist[nx][ny] < 0:
                dist[nx][ny] = dist[x][y] + 1; dq.append((nx, ny))
    return str(dist[r - 1][c - 1])
def big_maze():
    while True:
        rows = [list(x) for x in rgrid(150, 150, 0.28, ".#")]
        rows[0][0] = rows[-1][-1] = '.'; g = grid_in([''.join(x) for x in rows])
        if grid_bfs(g) != "-1": return g
add("Shortest Path in a Maze", "medium",
    D("A maze has open cells `.` and walls `#`. Starting at the top-left cell, find the fewest moves (up, down, left, right) to reach the bottom-right cell.",
      ["Line 1: rows `r` and columns `c` (1 ≤ r, c ≤ 300)", "Next `r` lines: a string of `c` characters, each `.` or `#`. The start and end cells are always `.`"],
      ["The minimum number of moves, or `-1` if the end cannot be reached."]),
    grid_bfs, [grid_in(["...", ".#.", "..."]), grid_in([".#", "#."]), "1 1\n.\n", grid_in(["..#.", "#.#.", "#...", "###."]), big_maze()])

# ------------------------------------------------------------------ HARD (12)
def lis(s):
    tails = []
    for x in ints(s)[1:]:
        i = bisect.bisect_left(tails, x)
        if i == len(tails): tails.append(x)
        else: tails[i] = x
    return str(len(tails))
add("Longest Increasing Subsequence", "hard",
    D("Find the length of the longest strictly increasing subsequence. A subsequence keeps the original order but may skip elements.",
      ["Line 1: `n` (1 ≤ n ≤ 100000)", "Line 2: `n` integers"], ["The length of the longest strictly increasing subsequence."]),
    lis, [A([10, 9, 2, 5, 3, 7, 101, 18]), A([0, 1, 0, 3, 2, 3]), A([7, 7, 7]), A([5]), A(ri(0, 10**6, BIG))])

def edit(s):
    a, b = s.split(); prev = list(range(len(b) + 1))
    for i in range(1, len(a) + 1):
        cur = [i] + [0] * len(b)
        for j in range(1, len(b) + 1):
            cur[j] = min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (a[i - 1] != b[j - 1]))
        prev = cur
    return str(prev[-1])
add("Edit Distance", "hard",
    D("The edit distance between two words is the fewest single-letter insertions, deletions or replacements needed to turn the first into the second.",
      ["Line 1: the first word", "Line 2: the second word (lowercase letters, 1 to 1000 each)"], ["The edit distance."]),
    edit, ["horse\nros\n", "intention\nexecution\n", "a\na\n", "abc\nxyz\n", rs("abcd", 700) + "\n" + rs("abcd", 650) + "\n"])

def knap(s):
    t = ints(s); n, W = t[0], t[1]; dp = [0] * (W + 1)
    for i in range(n):
        w, v = t[2 + 2 * i], t[3 + 2 * i]
        for c in range(W, w - 1, -1): dp[c] = max(dp[c], dp[c - w] + v)
    return str(dp[W])
def kn_in(W, items): return f"{len(items)} {W}\n" + "\n".join(f"{w} {v}" for w, v in items) + "\n"
add("0/1 Knapsack", "hard",
    D("You have `n` items, each with a weight and a value, and a bag that holds total weight `W`. Each item can be taken at most once. Maximize the total value.",
      ["Line 1: `n` (1 ≤ n ≤ 100) and `W` (1 ≤ W ≤ 10000)", "Next `n` lines: an item's weight and value"], ["The maximum total value."]),
    knap, [kn_in(50, [(10, 60), (20, 100), (30, 120)]), kn_in(5, [(10, 100)]), kn_in(10, [(5, 10), (4, 40), (6, 30), (3, 50)]),
           kn_in(10000, [(R.randint(1, 500), R.randint(1, 1000)) for _ in range(100)]), kn_in(7000, [(R.randint(50, 900), R.randint(1, 1000)) for _ in range(100)])])

def rand_graph(n, m, maxw):
    seen, lst = set(), []; nodes = list(range(1, n + 1)); R.shuffle(nodes)
    for i in range(1, n):
        u, v = nodes[R.randint(0, i - 1)], nodes[i]; lst.append((u, v, R.randint(1, maxw))); seen.add((min(u, v), max(u, v)))
    while len(lst) < m:
        u, v = R.randint(1, n), R.randint(1, n)
        if u == v or (min(u, v), max(u, v)) in seen: continue
        seen.add((min(u, v), max(u, v))); lst.append((u, v, R.randint(1, maxw)))
    R.shuffle(lst); return lst
def g_in(n, edges):
    body = "\n".join(' '.join(map(str, e)) for e in edges)
    return f"{n} {len(edges)}\n{body}\n" if body else f"{n} 0\n"
def dijkstra(s):
    t = ints(s); n, m = t[0], t[1]; adj = [[] for _ in range(n + 1)]
    for i in range(m):
        u, v, w = t[2 + 3 * i:5 + 3 * i]; adj[u].append((v, w)); adj[v].append((u, w))
    INF = float('inf'); d = [INF] * (n + 1); d[1] = 0; h = [(0, 1)]
    while h:
        du, u = heapq.heappop(h)
        if du > d[u]: continue
        for v, w in adj[u]:
            if du + w < d[v]: d[v] = du + w; heapq.heappush(h, (d[v], v))
    return ' '.join(str(d[i]) if d[i] < INF else "-1" for i in range(1, n + 1))
add("Shortest Paths (Dijkstra)", "hard",
    D("A road network has `n` towns and `m` two-way roads with lengths. Find the shortest distance from town 1 to every town.",
      ["Line 1: `n` and `m` (1 ≤ n ≤ 100000, 0 ≤ m ≤ 200000)", "Next `m` lines: `u v w`, a road between towns `u` and `v` of length `w` (1 ≤ w ≤ 10^6)"],
      ["`n` numbers separated by spaces: the distance to towns 1 through `n`, or `-1` if a town cannot be reached."]),
    dijkstra, ["5 6\n1 2 4\n1 3 1\n3 2 2\n2 4 5\n3 4 8\n4 5 3\n", "4 2\n1 2 5\n3 4 1\n", "1 0\n", g_in(300, rand_graph(300, 900, 50)), g_in(2000, rand_graph(2000, 8000, 1000))])

def topo(s):
    t = ints(s); n, m = t[0], t[1]; adj = [[] for _ in range(n + 1)]; indeg = [0] * (n + 1)
    for i in range(m):
        u, v = t[2 + 2 * i], t[3 + 2 * i]; adj[u].append(v); indeg[v] += 1
    h = [i for i in range(1, n + 1) if indeg[i] == 0]; heapq.heapify(h); out = []
    while h:
        u = heapq.heappop(h); out.append(u)
        for v in adj[u]:
            indeg[v] -= 1
            if indeg[v] == 0: heapq.heappush(h, v)
    return ' '.join(map(str, out)) if len(out) == n else "-1"
def big_dag(n, m):
    perm = list(range(1, n + 1)); R.shuffle(perm); seen = set()
    while len(seen) < m:
        i, j = sorted(R.sample(range(n), 2)); seen.add((perm[i], perm[j]))
    e = list(seen); R.shuffle(e); return e
def dag_in(n, edges):
    body = "\n".join(f"{u} {v}" for u, v in edges)
    return f"{n} {len(edges)}\n{body}\n" if body else f"{n} 0\n"
add("Course Order", "hard",
    D("There are `n` courses and `m` rules `u v` meaning course `u` must be taken before course `v`. Print an order that respects every rule. If several orders work, print the one that is smallest when read left to right (compare the first course, then the second, and so on).",
      ["Line 1: `n` and `m` (1 ≤ n ≤ 100000, 0 ≤ m ≤ 200000)", "Next `m` lines: `u v`"], ["The order, separated by spaces, or `-1` if the rules contain a cycle."]),
    topo, ["4 3\n1 2\n1 3\n3 4\n", "6 6\n6 3\n6 1\n5 1\n5 2\n3 4\n4 2\n", "3 3\n1 2\n2 3\n3 1\n", "3 0\n", dag_in(300, big_dag(300, 900)), dag_in(2000, big_dag(2000, 6000))])

def inversions(s):
    a = ints(s)[1:]
    def sort(x):
        if len(x) <= 1: return x, 0
        mid = len(x) // 2; l, cl = sort(x[:mid]); r, cr = sort(x[mid:]); i = j = c = 0; out = []
        while i < len(l) and j < len(r):
            if l[i] <= r[j]: out.append(l[i]); i += 1
            else: out.append(r[j]); j += 1; c += len(l) - i
        out += l[i:] + r[j:]; return out, cl + cr + c
    return str(sort(a)[1])
add("Count Inversions", "hard",
    D("An inversion is a pair of positions `i < j` where the value at `i` is greater than the value at `j`. Count the inversions in a list.",
      ["Line 1: `n` (1 ≤ n ≤ 100000)", "Line 2: `n` integers"], ["The number of inversions. It can exceed 32 bits."]),
    inversions, [A([2, 4, 1, 3, 5]), A([5, 4, 3, 2, 1]), A([1, 2, 3]), A([1]), A(ri(0, 10**9, BIG)), A(list(range(BIG, 0, -1)))])

def lps(s):
    s = s.strip(); best = 1
    for c in range(len(s)):
        for l, r in ((c, c), (c, c + 1)):
            while l >= 0 and r < len(s) and s[l] == s[r]: l -= 1; r += 1
            best = max(best, r - l - 1)
    return str(best)
add("Longest Palindromic Substring", "hard",
    D("Find the length of the longest substring that reads the same forwards and backwards.",
      ["One string of lowercase letters, 1 to 2000 characters."], ["The length of the longest palindromic substring."]),
    lps, ["babad\n", "cbbd\n", "a\n", "forgeeksskeegfor\n", rs("ab", 2000) + "\n", "a" * 1500 + "b" + "a" * 400 + "\n"])

def mst(s):
    t = ints(s); n, m = t[0], t[1]; edges = sorted((t[4 + 3 * i], t[2 + 3 * i], t[3 + 3 * i]) for i in range(m)); par = list(range(n + 1))
    def find(x):
        while par[x] != x: par[x] = par[par[x]]; x = par[x]
        return x
    tot = 0
    for w, u, v in edges:
        a, b = find(u), find(v)
        if a != b: par[a] = b; tot += w
    return str(tot)
add("Minimum Spanning Tree", "hard",
    D("Towns must be connected by cables so that every town can reach every other. Given the possible cables and their costs, find the cheapest total cost that connects all towns.",
      ["Line 1: `n` and `m` (1 ≤ n ≤ 100000, 0 ≤ m ≤ 200000)", "Next `m` lines: `u v w`, a possible cable between `u` and `v` costing `w` (1 ≤ w ≤ 10^6)", "The towns can always be connected."],
      ["The minimum total cost."]),
    mst, ["4 5\n1 2 1\n2 3 2\n3 4 3\n1 4 4\n1 3 2\n", "1 0\n", "2 1\n1 2 7\n", g_in(300, rand_graph(300, 900, 10**6)), g_in(2000, rand_graph(2000, 8000, 10**6))])

def rain(s):
    h = ints(s)[1:]; l, r = 0, len(h) - 1; lm = rm = tot = 0
    while l < r:
        if h[l] < h[r]:
            lm = max(lm, h[l]); tot += lm - h[l]; l += 1
        else:
            rm = max(rm, h[r]); tot += rm - h[r]; r -= 1
    return str(tot)
add("Trapping Rain Water", "hard",
    D("A row of bars has the given heights, each of width 1. After rain, water collects between the bars. Compute the total water trapped.",
      ["Line 1: `n` (1 ≤ n ≤ 100000)", "Line 2: `n` heights (0 ≤ height ≤ 10^5)"], ["The total units of water trapped."]),
    rain, [A([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]), A([4, 2, 0, 3, 2, 5]), A([1]), A([3, 3, 3]), A(ri(0, 1000, BIG))])

def nqueens(s):
    n = int(s); full = (1 << n) - 1
    def go(cols, d1, d2):
        if cols == full: return 1
        cnt, avail = 0, full & ~(cols | d1 | d2)
        while avail:
            b = avail & -avail; avail -= b
            cnt += go(cols | b, ((d1 | b) << 1) & full, (d2 | b) >> 1)
        return cnt
    return str(go(0, 0, 0))
add("N-Queens", "hard",
    D("Place `n` queens on an `n × n` chessboard so that no two attack each other (no shared row, column or diagonal). Count the distinct arrangements.",
      ["A single integer `n` (1 ≤ n ≤ 11)"], ["The number of valid arrangements."]),
    nqueens, ["1\n", "4\n", "5\n", "6\n", "8\n", "10\n", "11\n"])

def median2(s):
    t = ints(s); n, m = t[0], t[1]; x = sorted(t[2:2 + n] + t[2 + n:2 + n + m]); k = len(x)
    return f"{x[k // 2]:.1f}" if k % 2 else f"{(x[k // 2 - 1] + x[k // 2]) / 2:.1f}"
add("Median of Two Sorted Arrays", "hard",
    D("Two lists are each sorted in increasing order. Find the median of all their numbers combined. For an even count, the median is the average of the two middle values.",
      ["Line 1: `n` and `m` (1 ≤ n, m ≤ 100000)", "Line 2: the first list", "Line 3: the second list"], ["The median with exactly one digit after the decimal point, for example `2.0` or `2.5`."]),
    median2, [ms_in([1, 3], [2]), ms_in([1, 2], [3, 4]), ms_in([0, 0], [0, 0]), ms_in([-5, -3], [-4]),
              ms_in(sorted(ri(-10**9, 10**9, 8000)), sorted(ri(-10**9, 10**9, 7001)))])

def sliding(s):
    t = ints(s); n, k = t[0], t[1]; a = t[2:2 + n]; dq = deque(); out = []
    for i, x in enumerate(a):
        while dq and a[dq[-1]] <= x: dq.pop()
        dq.append(i)
        if dq[0] <= i - k: dq.popleft()
        if i >= k - 1: out.append(a[dq[0]])
    return ' '.join(map(str, out))
def sw_in(a, k): return f"{len(a)} {k}\n{' '.join(map(str, a))}\n"
add("Sliding Window Maximum", "hard",
    D("A window of size `k` slides across a list from left to right. Report the maximum value inside the window at every position.",
      ["Line 1: `n` and `k` (1 ≤ k ≤ n ≤ 100000)", "Line 2: `n` integers"], ["`n - k + 1` numbers separated by spaces."]),
    sliding, [sw_in([1, 3, -1, -3, 5, 3, 6, 7], 3), sw_in([1], 1), sw_in([4, 2, 12, 3], 4), sw_in([9, 8, 7, 6, 5], 2), sw_in(ri(-10**4, 10**4, BIG), 500)])

# ------------------------------------------------------------------ self-tests
def brute_check():
    r = random.Random(7)
    for _ in range(200):
        n = r.randint(1, 12); a = [r.randint(-6, 6) for _ in range(n)]
        assert inversions(A(a)) == str(sum(a[i] > a[j] for i in range(n) for j in range(i + 1, n)))
        dp = [1] * n
        for i in range(n):
            for j in range(i):
                if a[j] < a[i]: dp[i] = max(dp[i], dp[j] + 1)
        assert lis(A(a)) == str(max(dp))
        assert kadane(A(a)) == str(max(sum(a[i:j]) for i in range(n) for j in range(i + 1, n + 1)))
        k = r.randint(-5, 5); assert sub_k(sk_in(a, k)) == str(sum(sum(a[i:j]) == k for i in range(n) for j in range(i + 1, n + 1)))
        w = r.randint(1, n); assert sliding(sw_in(a, w)) == ' '.join(str(max(a[i:i + w])) for i in range(n - w + 1))
        h = [abs(x) for x in a]
        assert rain(A(h)) == str(sum(max(0, min(max(h[:i + 1]), max(h[i:])) - h[i]) for i in range(n)))
        st = ''.join(r.choice("ab") for _ in range(n))
        assert lps(st) == str(max(len(st[i:j]) for i in range(n) for j in range(i + 1, n + 1) if st[i:j] == st[i:j][::-1]))
    for _ in range(100):
        n = r.randint(1, 7); items = [(r.randint(1, 6), r.randint(1, 9)) for _ in range(n)]; W = r.randint(1, 15)
        best = max(sum(items[i][1] for i in range(n) if m >> i & 1) for m in range(1 << n) if sum(items[i][0] for i in range(n) if m >> i & 1) <= W)
        assert knap(kn_in(W, items)) == str(best)
        nn = r.randint(2, 7); e = rand_graph(nn, r.randint(nn - 1, nn * (nn - 1) // 2), 9)
        d = [10**9] * (nn + 1); d[1] = 0
        for _ in range(nn):
            for u, v, w in e:
                d[u] = min(d[u], d[v] + w); d[v] = min(d[v], d[u] + w)
        assert dijkstra(g_in(nn, e)) == ' '.join(str(x) for x in d[1:])
    for n_, exp in [(1, 1), (4, 2), (5, 10), (6, 4), (8, 92), (10, 724), (11, 2680)]: assert nqueens(str(n_)) == str(exp)
    assert edit("intention execution") == "5" and count_primes(10**6) == 78498
    assert from_roman("MCMXCIV") == 1994 and fib(90) == 2880067194370816120

# ------------------------------------------------------------------ output
STARTER = {
    "python": "import sys\n\ndef main():\n    data = sys.stdin.read().split()\n    # write your solution here\n\nmain()\n",
    "javascript": 'const data = require("fs").readFileSync(0, "utf8").split(/\\s+/).filter(Boolean);\n// write your solution here\n',
    "cpp": "#include <bits/stdc++.h>\nusing namespace std;\n\nint main() {\n    ios::sync_with_stdio(false);\n    cin.tie(nullptr);\n    // write your solution here\n    return 0;\n}\n",
    "java": "import java.util.*;\n\npublic class Main {\n    public static void main(String[] args) {\n        Scanner sc = new Scanner(System.in);\n        // write your solution here\n    }\n}\n",
}
LIMITS = {"easy": 600, "medium": 900, "hard": 1500}

def main():
    brute_check()
    slugs = [p["slug"] for p in P]; assert len(slugs) == len(set(slugs))
    out = ["-- Generated by tools/gen_problems.py. Expected outputs come from reference solutions.",
           "-- Safe to re-run: existing problems (matched by slug) are skipped.\n"]
    for p in P:
        cases, expected = [], []
        for i, inp in enumerate(p["tests"]):
            exp = p["solve"](inp); assert exp == exp.strip() and exp != "", (p["slug"], i, exp[:40])
            expected.append(exp); cases.append({"input": inp, "expected_output": exp, "is_hidden": i > 0})
        assert len(cases) >= 4 and len(set(expected)) >= 2, p["slug"]
        assert '$md$' not in p["desc"] and '$j$' not in json.dumps(cases)
        ex = [{"input": p["tests"][0].rstrip("\n"), "output": expected[0]}]
        out.append(f"insert into problems (title, slug, description, difficulty, time_limit_sec, examples, test_cases) values (\n"
                   f"  $t${p['title']}$t$, '{p['slug']}', $md${p['desc']}$md$, '{p['diff']}', {LIMITS[p['diff']]},\n"
                   f"  $j${json.dumps(ex)}$j$::jsonb,\n  $j${json.dumps(cases, separators=(',', ':'))}$j$::jsonb\n) on conflict (slug) do nothing;\n")
    out.append(f"update problems set starter_code = $j${json.dumps(STARTER)}$j$::jsonb where starter_code = '{{}}'::jsonb;\n")
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "backend", "src", "db", "seed.sql")
    with open(path, "w", encoding="utf-8", newline="\n") as f: f.write("\n".join(out))
    c = Counter(p["diff"] for p in P)
    print(f"{len(P)} problems: {dict(c)}; seed.sql = {os.path.getsize(path) / 1024:.0f} KB")

if __name__ == "__main__":
    main()
