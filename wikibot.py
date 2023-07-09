import wikipedia


def scrape(title,length=1):
    result = wikipedia.summary(title,sentences=length)
    return result

print(scrape("Microsoft",length=2))
