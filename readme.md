

## Wordsegment Polish Corpus

This repository contains Polish unigram and bigram frequency files for use with the **[wordsegment](https://grantjenks.com/docs/wordsegment/)** library.
They were created from the **2023 Polish Wikipedia dump** ([Hugging Face dataset](https://huggingface.co/datasets/chrisociepa/wikipedia-pl-20230401)).


```
('Einstein to twórca szczególnej teorii względności, która ulepszyła mechanikę '
 'Newtona i zastąpiła w tej korekcyjnej roli teorię eteru Lorentza. Autor '
 'wynikającej z STW równoważności masy i energii, czasem formułowanej słynnym '
 'wzorem E = mc2. Został on potwierdzony przez reakcje subatomowe, np. '
 'jądrowe; doprowadziło to do rewizji zasady zachowania masy, samego pojęcia '
 'materii i otworzyło epokę jądrowej broni oraz energetyki.')

text = 'Einsteintotwórcaszczególnejteoriiwzględności,któraulepszyłamechanikęNewtonaizastąpiławtejkorekcyjnejroliteorięeteruLorentza.AutorwynikającejzSTWrównoważnościmasyienergii,czasemformułowanejsłynnymwzoremE=mc2.Zostałonpotwierdzonyprzezreakcjesubatomowe,np.jądrowe;doprowadziłotodorewizjizasadyzachowaniamasy,samegopojęciamateriiiotworzyłoepokęjądrowejbroniorazenergetyki.'

wordsegment.segment(text)
['einstein',
 'to',
 'twórca',
 'szczególnej',
 'teorii',
 'względności',
 'która',
 'ulepszyła',
 'mechanikę',
 'newtona',
 'i',
 'zastąpiła',
 'w',
 'tej',
 'korekcyjnej',
 'rol',
 'i',
 'teorię',
 'eteru',
 'lorentza',
 'autor',
 'wynikającej',
 'z',
 'st',
 'w',
...
 'epokę',
 'jądrowej',
 'broni',
 'oraz',
 'energetyki']
 ```