---
slug: factors-and-multiples
title: "Factors and Multiples"
order: 7
summary: "Factors, multiples, primes, divisibility tests, prime factorisation, co-prime numbers."
---

<!-- Migrated from mathematics.md. Math expressions like "2 / 3" or "2 * 3" should be converted to KaTeX ($\frac{2}{3}$, $2 \times 3$) during review. -->

# Factors and Multiples
## Factor / Divisor

If a number **divides another number exactly**, it is called a **factor** or **divisor** of that number.

Example: **4 is a factor of 12** because 12 / 4 = 3 with no remainder.

Important:
- **1 is a factor of every number.**
- **Every number is a factor of itself.**
- **Factors are finite.** A number has a limited number of factors.
- To check if a number is a factor, divide and see if the **remainder is 0**.

Example: Factors of 24 are 1, 2, 3, 4, 6, 8, 12, 24.

## Multiple

A **multiple** of a number is obtained by multiplying it by 1, 2, 3, 4, ...

Example: Multiples of 5 are 5, 10, 15, 20, 25, ...

Important:
- **Multiples are infinite.**
- **A number is always a multiple of itself.**
- If a number is divisible by another number, then it is a **multiple** of that number.

Example: 24 is a multiple of 4 because 24 = 4 * 6.

## Common Multiples

**Common multiples** are numbers that are multiples of two or more given numbers.

Example:
- Multiples of 3: 3, 6, 9, 12, 15, 18, 21, 24, 27, 30, ...
- Multiples of 5: 5, 10, 15, 20, 25, 30, ...
- Common multiples of 3 and 5: 15, 30, 45, 60, ...

The **first common multiple** is the **smallest common multiple**. Later this is called **LCM** or **least common multiple**.

## Common Factors

**Common factors** are numbers that are factors of two or more given numbers.

Example:
- Factors of 14: 1, 2, 7, 14
- Factors of 36: 1, 2, 3, 4, 6, 9, 12, 18, 36
- Common factors of 14 and 36: 1, 2

## Prime Numbers

A **prime number** has **exactly two factors**: 1 and itself.

Examples: 2, 3, 5, 7, 11, 13, 17, 19.

Important:
- **1 is not a prime number.**
- **2 is the only even prime number.**
- **Every prime number except 2 is odd.**
- A prime number still has factors: **1 and itself**.

## Composite Numbers

A **composite number** has **more than two factors**.

Examples: 4, 6, 8, 9, 10, 12, 14, 15, 16, 18, 20.

Important:
- **All even numbers greater than 2 are composite.**
- A **product of two or more prime numbers is composite**.
- Composite numbers can be broken down into smaller factors.

## 1 Is Special

**1 is neither prime nor composite.**

Reason:
- Prime numbers have **exactly 2 factors**.
- Composite numbers have **more than 2 factors**.
- **1 has only 1 factor: itself.**

## Twin Primes

**Twin primes** are pairs of prime numbers that **differ by 2**.

Examples:
- 3 and 5
- 5 and 7
- 11 and 13
- 17 and 19
- 29 and 31
- 41 and 43
- 59 and 61
- 71 and 73

## Co-prime Numbers

Two numbers are **co-prime** if their **only common factor is 1**.

Examples:
- 4 and 9 are co-prime.
- 18 and 35 are co-prime.
- 15 and 39 are not co-prime because both have 3 as a factor.

Important:
- **Co-prime numbers do not need to be prime individually.**
- **Any two different prime numbers are co-prime.**
- If two numbers are co-prime, their **first common multiple is their product**.

Example:
- 3 and 5 are co-prime.
- First common multiple = 15.
- Product = 3 * 5 = 15.

If numbers are not co-prime, the **first common multiple is usually less than their product**.

Example:
- 3 and 6 are not co-prime.
- Product = 18.
- First common multiple = 6.

## Prime Factorisation

**Prime factorisation** means writing a number as a **product of prime numbers**.

Example:
56 = 2 * 2 * 2 * 7

Here, **2 and 7 are the prime factors** of 56.

Important:
- **Every number greater than 1 has a prime factorisation.**
- **1 has no prime factorisation.**
- A prime number's prime factorisation is **just itself**.
- **Prime factorisation is unique** except for the order of factors.

Example:
36 = 2 * 2 * 3 * 3

**The order does not matter:**
2 * 2 * 3 * 3 = 3 * 2 * 3 * 2 = 36

## Prime Factorisation of a Product

To find the prime factorisation of a product, **factorise each number** and **combine all prime factors**.

Example:
72 = 12 * 6

12 = 2 * 2 * 3

6 = 2 * 3

So:
72 = 2 * 2 * 3 * 2 * 3 = 2 * 2 * 2 * 3 * 3

## Using Prime Factorisation to Check Co-prime Numbers

Find **prime factorisations of both numbers**.

If there is **no common prime factor**, the numbers are **co-prime**.

Example:
80 = 2 * 2 * 2 * 2 * 5

63 = 3 * 3 * 7

**No common prime factor**, so 80 and 63 are **co-prime**.

Example:
56 = 2 * 2 * 2 * 7

63 = 3 * 3 * 7

**Common prime factor is 7**, so 56 and 63 are **not co-prime**.

## Using Prime Factorisation to Check Divisibility

A number is divisible by another number if the **second number's full prime factorisation is included** in the first number's prime factorisation.

Example:
168 = 2 * 2 * 2 * 3 * 7

12 = 2 * 2 * 3

Since 168 contains all prime factors of 12, **168 is divisible by 12**.

Example:
42 = 2 * 3 * 7

12 = 2 * 2 * 3

**42 is not divisible by 12** because 12 needs **two 2s**, but 42 has only one 2.

**Repeated prime factors matter.**

## Divisibility Tests

**Divisible by 10:**
- Last digit is 0.

**Divisible by 5:**
- Last digit is 0 or 5.

**Divisible by 2:**
- Last digit is 0, 2, 4, 6, or 8.

**Divisible by 4:**
- The number formed by the last two digits is divisible by 4.

Example:
8536 is divisible by 4 because 36 is divisible by 4.

**Divisible by 8:**
- The number formed by the last three digits is divisible by 8.

Example:
8560 is divisible by 8 because 560 is divisible by 8.

## Useful Chapter Patterns

**Common multiple pattern:**
- For numbers a and b, common multiples appear at regular gaps.

**Co-prime product pattern:**
- If a and b are co-prime, first common multiple = a * b.

**Divisibility inclusion pattern:**
- To check if A is divisible by B, all prime factors of B must appear in A with enough repeats.

## Common Mistakes

- Saying **1 is prime**. It is neither prime nor composite.
- Saying **prime numbers have no factors**. They have exactly two factors.
- Saying **all odd numbers are prime**. 9, 15, 21, 25 are odd but composite.
- Saying **all even numbers are composite**. 2 is even and prime.
- Ignoring **repeated factors** in divisibility. 12 = 2 * 2 * 3 needs two 2s.
- Confusing **factors and multiples**. Factors divide the number; multiples are made by multiplying the number.
