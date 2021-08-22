from selenium import webdriver

with webdriver.Firefox() as driver:
    driver.get('http://localhost:8985')

    date = driver.find_element_by_css_selector('.date').text
    print(f'FX rates for {date}')

    tds = driver.find_elements_by_tag_name('td')
    for i in range(0, len(tds), 2):
        symbol = tds[i].text
        ratio = float(tds[i+1].text)
        print(f'- {symbol} -> {ratio:.2f}')
