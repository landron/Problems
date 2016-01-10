import Data.Char
import Data.Typeable
import System.IO

assert :: Bool -> a -> a
assert False x = error "assertion failed!"
assert _     x = x

--This does not work for big numbers

factorial :: Int -> Int
factorial 0 = 1
factorial n = n * factorial (n-1)

--The easy way: using Integer

big_factorial :: Int -> Integer
big_factorial 0 = 1
big_factorial n = toInteger n * big_factorial (n-1)

--The hard way: using Int arrays

add_digit :: Int -> Int -> (Int, Bool)
add_digit c d = ((c+d) `mod` 10, 10 <= (c+d))

add_digits :: Int -> Int -> Int -> (Int, Bool)
add_digits c d e = add_digit (c+d) e

big_add_digit :: [Int] -> Int -> [Int]
big_add_digit [] d = [d]
big_add_digit u d
    | carry = (big_add_digit (init u) 1) ++ [lastC]
    | otherwise = (init u) ++ [lastC]
    where
        (lastC, carry) = add_digit (last u) d

big_sum_inc :: [Int] -> [Int] -> Int -> [Int]
big_sum_inc [] [] 0 = []
big_sum_inc [] v d = big_add_digit v d
big_sum_inc u [] d = big_add_digit u d
big_sum_inc u v d
    | carry     = (big_sum_inc (init u) (init v) 1) ++ [lastC]
    | otherwise = (big_sum_inc (init u) (init v) 0) ++ [lastC]
    where
        (lastC, carry) = add_digits (last u) (last v) d

big_sum :: [Int] -> [Int] -> [Int]
big_sum u v = big_sum_inc u v 0

int_to_array :: Int -> [Int]
int_to_array n 
    | n < 10 = [n]
    | otherwise = (int_to_array $ quot n 10) ++ [n `mod` 10]

power_of_ten :: Int -> Int -> [Int]
power_of_ten n m = (int_to_array n) ++ take m (repeat 0)

big_product_pow :: [Int] -> [Int] -> Int -> Int -> [Int]
big_product_pow [] v _ _ = v
big_product_pow u v d n = big_product_pow (init u) acc d (n+1)
        where
            acc = big_sum v (power_of_ten (last u * d) n)

big_product :: [Int] -> Int -> [Int]
big_product u m = big_product_pow u [] m 0

big_factorial_array_base :: Int -> [Int]
big_factorial_array_base 0 = [1]
big_factorial_array_base n = big_product (big_factorial_array_base $ n-1) n

convert_array_to_string :: [Int] -> String
convert_array_to_string [] = ""
convert_array_to_string u = (show $ head u) ++ (convert_array_to_string $ tail u)

big_factorial_array :: Int -> String
big_factorial_array n = convert_array_to_string $ big_factorial_array_base n 

--The hardest way: using strings

add_digit_to_char :: Char -> Int -> (Char, Bool)
add_digit_to_char c d = (last $ show (fst aSum), snd aSum)
    where aSum = add_digit (digitToInt c) d

big_add_digit_s :: String -> Int -> String
big_add_digit_s "" d = show d
big_add_digit_s u d
    | carry = (big_add_digit_s (init u) 1) ++ [lastC]
    | otherwise = (init u) ++ [lastC]
    where
        (lastC, carry) = add_digit_to_char (last u) d

add_chars :: Char -> Char -> Int -> (Char, Bool)
add_chars c d e = (last $ show aSum, 10 <= aSum)
    where   
        aSum = digitToInt c + digitToInt d + e

big_sum_inc_s :: String -> String -> Int -> String
big_sum_inc_s "" "" 0 = ""
big_sum_inc_s "" v d = big_add_digit_s v d
big_sum_inc_s u "" d = big_add_digit_s u d
big_sum_inc_s u v d
    | carry     = (big_sum_inc_s (init u) (init v) 1) ++ [lastC]
    | otherwise = (big_sum_inc_s (init u) (init v) 0) ++ [lastC]
    where
        (lastC, carry) = add_chars (last u) (last v) d

big_sum_s :: String -> String -> String
big_sum_s u v = big_sum_inc_s u v 0

power_of_ten_s :: Int -> Int -> String
power_of_ten_s n m = show n ++ take m (repeat '0')

big_product_pow_s :: String -> String -> Int -> Int -> String
big_product_pow_s "" v _ _ = v
big_product_pow_s u v d n = big_product_pow_s (init u) acc d (n+1)
        where
            acc = big_sum_s v (power_of_ten_s ((digitToInt $ last u) * d) n)

big_product_s :: String -> Int -> String
big_product_s u m = big_product_pow_s u "" m 0

big_factorial_string :: Int -> String
big_factorial_string 0 = "1"
big_factorial_string n = big_product_s (big_factorial_string $ n-1) n

--IO

readInt :: IO Int
readInt = readLn

repeatNTimes 0 _ = return ()
repeatNTimes n action = do
    action
    repeatNTimes (n-1) action

----avoid showing quotes for strings
--get_factorial_wrap :: (Int -> a) -> Int -> Bool -> a
--get_factorial_wrap factorialF number doShow
--    | doShow = show result
--    | otherwise = result
--    where result = factorialF number

--get_factorial_wrap_2 factorialF number
--    | (typeOf result /= typeOf "") = show result
--    | otherwise = result
--    where result = factorialF number

get_factorial factorialF = do
    number <- readInt
    --print $ factorialF number
    putStrLn $ factorialF number

do_factorial factorialF = do
    lines <- readInt
    repeatNTimes lines (get_factorial factorialF)

validate =
    --good for 64-bit
    assert ((big_factorial 20) == toInteger (factorial 20))
    assert ((big_factorial 21) /= toInteger (factorial 21))
    --they take some time
    assert ((big_factorial 100) == (read (big_factorial_string 100) :: Integer))
    assert ((big_factorial 100) == (read (big_factorial_array 100) :: Integer))

    putStrLn "Validation done!"

{-
main    
-}

--  1.  it doesn't work for big numbers (see also validate)
--main = do_factorial $ show . factorial

--  2.  it works for big enough numbers
--main = do_factorial $ show . big_factorial

-- 3. it works for any given number, but it takes some time
--main = do_factorial big_factorial_string

-- 4. it works for any given number, but it takes some time
main = do_factorial big_factorial_array