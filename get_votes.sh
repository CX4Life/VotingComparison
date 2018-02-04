#!/usr/bin/env bash

cd ../congress
for year in range 2018 2017
do
    ./run votes --congress=115 --session=$year
done

for year in range 2016 2015
do
    ./run votes --congress=114 --session=$year
done

for year in range 2014 2013
do
    ./run votes --congress=113 --session=$year
done

for year in range 2012 2011
do
    ./run votes --congress=112 --session=$year
done

for year in range 2010 2009
do
    ./run votes --congress=111 --session=$year
done

for year in range 2008
do
    ./run votes --congress=110 --session=$year
done