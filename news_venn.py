import json, re
from collections import Counter

datafile = '~/Desktop/Archive/Programming/cbsi/hack_day_2014/stories_real.json'
f = open(datafile, 'r')
data = json.loads(f.read())

top_domains = []
for story in data:
    #print(story)
    p = re.compile("(\w+)- (.*)")
    dt = p.findall(story['name'])[0]
    domain = dt[0]
    top_domains.append(domain)

c = Counter(top_domains)
print(c)

domains = list(c)

#pre-create counter hash
counters = {}
for domain in domains:
    counters[domain] = {}
    for inner_domain in domains:
        if inner_domain != domain:
            counters[domain][inner_domain] = 0

# print(counters)
#
# exit(0)



for story in data:
    p = re.compile("(\w+)- (.*)")
    dt = p.findall(story['name'])[0]
    domain = dt[0]
    links = story['imports']
    for link in links:
        ld = p.findall(link)[0]
        link_domain = ld[0]
        if link_domain != domain:

            # add link from domain to link_domain
            counters[domain][link_domain] = counters[domain][link_domain] + 1
            # print("linking " + domain + " to " + link_domain)

print(counters)

domain_tuples = []
for key in counters:
    domain = key
    for key2 in counters[key]:
        domain_tuple = (domain, str(key2), str(counters[key][key2]))
        domain_tuples.append(domain_tuple)
        #print(domain + " " + str(key2) + " " + str(counters[key][key2]))


print(domain_tuples)
# final_tuple_array = []
# for domain_tuple in domain_tuples:
#     domain = domain_tuple[0]
#     second_domain  = domain_tuple[1]
#     for inner_tuple in domain_tuples:



exit(0)



