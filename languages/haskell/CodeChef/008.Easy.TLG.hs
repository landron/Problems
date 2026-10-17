import Data.Char
import System.IO

get_number_pos :: String -> Int -> String
get_number_pos "" _ = ""
get_number_pos s n
    | n > 0 = get_number_pos (drop n s) 0
    | head s >= '0' && head s <= '9' = [head s] ++ (get_number_pos (tail s) 0)
    | otherwise = ""

get_number :: String -> String
get_number s = get_number_pos s 0

first :: (a,b,c) -> a
first (x,_,_) =  x

second :: (a,b,c) -> b
second (_,y,_) =  y

third :: (a,b,c) -> c
third (_,_,z) =  z

repeatNTimes_base 0 current _ = do
    let result = (show $ first current) ++ " " ++ (show $ second current)
    putStrLn result
repeatNTimes_base n current action = do
    --writing the next line was the most difficult part (it's not a simple )
    next <- action current
    repeatNTimes_base (n-1) next action

repeatNTimes n action = repeatNTimes_base n (0,0,0) action

process_new_record diff 
    | diff < 0 = (2, negate diff, diff)
    | otherwise = (1, diff, diff)

process_current line current
    | abs diff > second current = process_new_record diff
    | otherwise = (first current, second current, diff)
    where
        player1_score = get_number line
        player2_score = get_number_pos line (length player1_score + 1)
        diff = (read player1_score :: Int) - (read player2_score :: Int) + third current

--process_lines :: (Int, Int, Int) -> IO (Int, Int, Int)
process_lines current = do
    line <- getLine
    --putStrLn line
    return (process_current line current)

readInt :: IO Int
readInt = readLn

main = do
    lines_no <- readInt
    repeatNTimes lines_no process_lines
    --putStrLn $ show lines_no