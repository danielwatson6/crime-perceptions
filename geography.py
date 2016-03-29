#!/usr/bin/env python
#coding: utf8 

survey_results = []

# Used within various iterations
crimes = ['Burglary', 'Mugging', 'Assault', 'Gun crime', 'Knife crime']
times = ['7am', '2pm', '11pm']

with open('survey.tsv') as f:
  content = f.readlines()
  for person in content[1:]:
    survey_results.append(person.split('\t'))

survey_analysis = {} # dict keys are the neighborhoods

# Compute frequencies
for p in survey_results:
  # Update count of people in neighborhood or create
  # empty data structure if it has not been recorded
  n = p[0]
  try:
    survey_analysis[n]['Number of surveyed people'] += 1
  except KeyError:
    survey_analysis[n] = {
      'Number of surveyed people': 1,
      'Patrols reported': {
        'Yes': 0,
        'No': 0
      },
      'Crime witnesses': {
        'Yes': 0,
        'No': 0
      },
      'Important things for safety': {
        'Well lit area': 0,
        'Knowledge of the area': 0,
        'Close to a main road': 0,
        'Alarms': 0,
        'Area monitored by police': 0,
        'Pleasant environment': 0,
        'Gardens and open space': 0,
        'Other people nearby': 0
      },
      'Safety perception per crime': {
        'Burglary': {'Frequencies':[0,0,0,0,0,0,0,0,0,0]},
        'Mugging': {'Frequencies':[0,0,0,0,0,0,0,0,0,0]},
        'Assault': {'Frequencies':[0,0,0,0,0,0,0,0,0,0]},
        'Gun crime': {'Frequencies':[0,0,0,0,0,0,0,0,0,0]},
        'Knife crime': {'Frequencies':[0,0,0,0,0,0,0,0,0,0]}
      },
      'Safety perception per daytime': {
        '7am': {'Frequencies':[0,0,0,0,0,0,0,0,0,0]},
        '2pm': {'Frequencies':[0,0,0,0,0,0,0,0,0,0]},
        '11pm': {'Frequencies':[0,0,0,0,0,0,0,0,0,0]}
      }
    }
  # Fill in data structure with data
  survey_analysis[n]['Patrols reported'][p[1]] += 1
  survey_analysis[n]['Crime witnesses'][p[2]] += 1
  for i in p[3].split(', '):
    survey_analysis[n]['Important things for safety'][i] += 1
  for i in range(5):
    print crimes[i]
    print survey_analysis[n]['Safety perception per crime'][crimes[i]]
    print ''
    survey_analysis[n]['Safety perception per crime'][crimes[i]]['Frequencies'][int(p[i+4])-1] += 1
  for i in range(3):
    survey_analysis[n]['Safety perception per daytime'][times[i]]['Frequencies'][int(p[i+9])-1] += 1

# Compute averages
for n in survey_analysis:
  def record(s, k, _sum, _n):
    survey_analysis[n]['Safety perception per %s' % s][k]['Average'] = float(_sum) / float(_n)
  crime_list = survey_analysis[n]['Safety perception per crime']
  for k,c in crime_list.iteritems():
    crime_avg = 0
    crime_avg_count = 0
    for f in range(10):
      crime_avg += (f+1) * c['Frequencies'][f]
      crime_avg_count += c['Frequencies'][f]
    record('crime', k, crime_avg, crime_avg_count)
  time_list = survey_analysis[n]['Safety perception per daytime']
  for k,t in time_list.iteritems():
    time_avg = 0
    time_avg_count = 0
    for f in range(10):
      time_avg += (f+1) * t['Frequencies'][f]
      time_avg_count += t['Frequencies'][f]
    record('daytime', k, time_avg, time_avg_count)

# Output
for neighborhood, props in survey_analysis.iteritems():
  print "Neighborhood: " + neighborhood
  for prop, value in props.iteritems():
    if type(value) in [int, float]:
      print prop + ": " + str(value)
    else: # type is always dict
      print prop + ":"
      for k,v in value.iteritems():
        if type(v) == dict:
          print "\t%s:" % k
          for k2,v2 in v.iteritems():
            print "\t\t{k}: {v}".format(k=k2,v=v2)
        else:
          print "\t{k}: {v}".format(k=k,v=v)
  print '' # newline
