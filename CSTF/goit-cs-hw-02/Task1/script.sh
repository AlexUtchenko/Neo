#!/bin/bash

# Список веб-сайтів для перевірки
websites=("https://google.com" "https://facebook.com" "https://twitter.com")

# Файл для збереження результатів
logfile="website_status.log"

# Очищення файлу логів перед використанням
> "$logfile"

# Перевірка кожного сайту
for site in "${websites[@]}"
do
    # Використання команди curl для перевірки доступності веб-сайту
    if curl -s -L --head  --request GET "$site" | grep "HTTP/2 200" > /dev/null
    then 
        echo "$site is UP" >> "$logfile"
    else
        echo "$site is DOWN" >> "$logfile"
    fi
done

# Вивід результатів
echo "Results have been written to $logfile"