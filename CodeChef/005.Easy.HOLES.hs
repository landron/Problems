import Data.Char
import System.IO

holes :: Char -> Int
holes ch 
    |   'B' == ch = 2
    |   elem ch "ADOPQR" = 1
--  |   otherwise = 0
    |   isUpper ch = 0
    |   otherwise = error "function defined only for upper case letters"

holesIn :: String -> Int
holesIn = sum . map holes

repeatNTimes 0 _ = return ()
repeatNTimes n action = do
  action
  repeatNTimes (n-1) action

findHolesInReadString = do
    line <- getLine
    print $ holesIn line

readInt :: IO Int
readInt = readLn

main = do
    lines <- readInt
    repeatNTimes lines findHolesInReadString