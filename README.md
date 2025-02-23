# Coreferee-it

Roadmap to coreferee-it: adding Italian to the languages available in [coreferee](https://github.com/explosion/coreferee).

If you want to contribute in this direction, you can get started by reading the introduction provided below. The most important section for the purposes of this repository is [4. Adding support for a new language](#adding-support-for-a-new-language). Out of the outlined steps, 1 and 2 are done, while 3 is underway (see [language_specific_rules.py](https://github.com/EmmaZanoli/coreferee-it/blob/87ba8132c16df9bad57e3bb4af24cb95aba7f8f3/coreferee/lang/it/language_specific_rules.py)).

_as of now, everything below this line is identical to the original [coreferee repository](https://github.com/explosion/coreferee)_

------

# Coreferee

Author: <a href="mailto:richard@explosion.ai">Richard Paul Hudson, Explosion AI</a>

- [1. Introduction](#introduction)
  - [1.1 The basic idea](#the-basic-idea)
  - [1.2 Getting started](#getting-started)
    - [1.2.1 English](#getting-started-en)
    - [1.2.2 French](#getting-started-fr)
    - [1.2.3 German](#getting-started-de)
    - [1.2.4 Polish](#getting-started-pl)
  - [1.3 Background information](#background-information)
  - [1.4 Facts and figures](#facts-and-figures)
    - [1.4.1 Covered relevant linguistic features](#covered-relevant-linguistic-features)
    - [1.4.2 Model performance](#model-performance)
- [2. Interacting with the data model](#interacting-with-the-data-model)
- [3. How it works](#how-it-works)
  - [3.1 General operation and rules](#general-operation-and-rules)
    - [3.1.1 Anaphor pair analysis](#anaphor-pair-analysis)
    - [3.1.2 Noun pair detection](#noun-pair-detection)
    - [3.1.3 Building the chains](#building-the-chains)
  - [3.2 The neural ensemble](#the-neural-ensemble)
- [4. Adding support for a new language](#adding-support-for-a-new-language)
- [5. Adding support for a custom spaCy model](#adding-support-for-a-custom-spaCy-model)
- [6. Version history]('#version-history')
  - [6.1 Version 1.0.0](#version-100)
  - [6.2 Version 1.0.1](#version-101)
  - [6.3 Version 1.1.0](#version-110)
  - [6.4 Version 1.1.1](#version-111)
  - [6.5 Version 1.1.2](#version-112)
  - [6.6 Version 1.1.3](#version-113)
  - [6.7 Version 1.2.0](#version-120)
- [7. Open issues/requests for assistance](#open-issues)

<a id="introduction"></a>

### 1. Introduction

<a id="the-basic-idea"></a>

#### 1.1 The basic idea

Coreferences are situations where two or more words within a text refer to the same entity, e.g. _**John** went home because **he** was tired_. Resolving coreferences is an important general task within the natural language processing field.

Coreferee is a Python 3 library (tested with versions 3.6—3.10) that is used together with [spaCy](https://spacy.io/) (tested with versions 3.0.0—3.3.0) to resolve coreferences within English, French, German and Polish texts. It is designed so that it is easy to add support for new languages. It uses a mixture of neural networks and programmed rules.

The library was originally developed at [msg systems](https://www.msg.group/en), but is now being maintained at [Explosion AI](https://explosion.ai).

<a id="getting-started"></a>

#### 1.2 Getting started

<a id="getting-started-en"></a>

##### 1.2.1 English

Presuming you have already installed [spaCy](https://spacy.io/) and one of the English spacy models, install Coreferee from the command line by typing:

```
python3 -m pip install coreferee
python3 -m coreferee install en
```

Note that:

- the required command may be `python` rather than `python3` on some operating systems;
- in order to use the transformer-based spaCy model `en_core_web_trf` with Coreferee, you will need to install the spaCy model `en_core_web_lg` as well (see the explanation [here](#model-performance)).

Then open a Python prompt (type `python3` or `python` at the command line):

```
>>> import coreferee, spacy
>>> nlp = spacy.load('en_core_web_trf')
>>> nlp.add_pipe('coreferee')
<coreferee.manager.CorefereeBroker object at 0x000002DE8E9256D0>
>>>
>>> doc = nlp("Although he was very busy with his work, Peter had had enough of it. He and his wife decided they needed a holiday. They travelled to Spain because they loved the country very much.")
>>>
>>> doc._.coref_chains.print()
0: he(1), his(6), Peter(9), He(16), his(18)
1: work(7), it(14)
2: [He(16); wife(19)], they(21), They(26), they(31)
3: Spain(29), country(34)
>>>
>>> doc[16]._.coref_chains.print()
0: he(1), his(6), Peter(9), He(16), his(18)
2: [He(16); wife(19)], they(21), They(26), they(31)
>>>
>>> doc._.coref_chains.resolve(doc[31])
[Peter, wife]
>>>
```

<a id="getting-started-fr"></a>

##### 1.2.2 French

Presuming you have already installed [spaCy](https://spacy.io/) and one of the French spacy models, install Coreferee from the command line by typing:

```
python3 -m pip install coreferee
python3 -m coreferee install fr
```

Note that the required command may be `python` rather than `python3` on some operating systems.

Then open a Python prompt (type `python3` or `python` at the command line):

```
>>> import coreferee, spacy
>>> nlp = spacy.load('fr_core_news_lg')
>>> nlp.add_pipe('coreferee')
<coreferee.manager.CorefereeBroker object at 0x000001F556B4FF10>
>>>
>>> doc = nlp("Même si elle était très occupée par son travail, Julie en avait marre. Alors, elle et son mari décidèrent qu'ils avaient besoin de vacances. Ils allèrent en Espagne car ils adoraient le pays")
>>>
>>> doc._.coref_chains.print()
0: elle(2), son(7), Julie(10), elle(17), son(19)
1: travail(8), en(11)
2: [elle(17); mari(20)], ils(23), Ils(29), ils(34)
3: Espagne(32), pays(37)
>>>
>>> doc[17]._.coref_chains.print()
0: elle(2), son(7), Julie(10), elle(17), son(19)
2: [elle(17); mari(20)], ils(23), Ils(29), ils(34)
>>>
>>> doc._.coref_chains.resolve(doc[34])
[Julie, mari]
>>>
```

<a id="getting-started-de"></a>

##### 1.2.3 German

Presuming you have already installed [spaCy](https://spacy.io/) and one of the German spacy models, install Coreferee from the command line by typing:

```
python3 -m pip install coreferee
python3 -m coreferee install de
```

Note that the required command may be `python` rather than `python3` on some operating systems.

Then open a Python prompt (type `python3` or `python` at the command line):

```
>>> import coreferee, spacy
>>> nlp = spacy.load('de_core_news_lg')
>>> nlp.add_pipe('coreferee')
<coreferee.manager.CorefereeBroker object at 0x0000026E84C63B50>
>>>
>>> doc = nlp("Weil er mit seiner Arbeit sehr beschäftigt war, hatte Peter davon genug. Er und seine Frau haben entschieden, dass ihnen ein Urlaub gut tun würde. Sie sind nach Spanien gefahren, weil ihnen das Land sehr gefiel.")
>>>
>>> doc._.coref_chains.print()
0: er(1), seiner(3), Peter(10), Er(14), seine(16)
1: Arbeit(4), davon(11)
2: [Er(14); Frau(17)], ihnen(22), Sie(29), ihnen(36)
3: Spanien(32), Land(38)
>>>
>>> doc[14]._.coref_chains.print()
0: er(1), seiner(3), Peter(10), Er(14), seine(16)
2: [Er(14); Frau(17)], ihnen(22), Sie(29), ihnen(36)
>>>
>>> doc._.coref_chains.resolve(doc[36])
[Peter, Frau]
>>>
```

<a id="getting-started-pl"></a>

##### 1.2.4 Polish

Presuming you have already installed [spaCy](https://spacy.io/) and one of the Polish spacy models, install Coreferee from the command line by typing:

```
python3 -m pip install coreferee
python3 -m coreferee install pl
```

Note that the required command may be `python` rather than `python3` on some operating systems.

Then open a Python prompt (type `python3` or `python` at the command line):

```
>>> import coreferee, spacy
>>> nlp = spacy.load('pl_core_news_lg')
>>> nlp.add_pipe('coreferee')
<coreferee.manager.CorefereeBroker object at 0x0000027304C63B50>
>>>
>>> doc = nlp("Ponieważ bardzo zajęty był swoją pracą, Janek miał jej dość. Postanowili z jego żoną, że potrzebują wakacji. Pojechali do Hiszpanii, bo bardzo im się ten kraj podobał.")
>>>
>>> doc._.coref_chains.print()
0: był(3), swoją(4), Janek(7), Postanowili(12), jego(14)
1: pracą(5), jej(9)
2: [Postanowili(12); żoną(15)], potrzebują(18), Pojechali(21), im(27)
3: Hiszpanii(23), kraj(30)
>>>
>>> doc[12]._.coref_chains.print()
0: był(3), swoją(4), Janek(7), Postanowili(12), jego(14)
2: [Postanowili(12); żoną(15)], potrzebują(18), Pojechali(21), im(27)
>>>
>>> doc._.coref_chains.resolve(doc[27])
[Janek, żoną]
>>>
```

<a id="background-information"></a>

#### 1.3 Background information

Handling coreference resolution successfully requires training corpora that have been manually annotated with coreferences. The [state of the art in coreference resolution](https://paperswithcode.com/sota/coreference-resolution-on-conll-2012) is progressing rapidly, but is largely focussed on techniques that require training corpora that are larger than what is available for most languages and software developers. The [CONLL 2012 training corpus](https://cemantix.org/conll/2012/task-description.html), which is most widely used, has the following restrictions:

- CONLL 2012 covers English, Chinese and Arabic; there is nothing of comparable size for most other languages. For example, the [corpus](#model-performance) we used to train Coreferee for German is around a tenth of the size of CONLL 2012;

- CONLL 2012 is not publicly available and has a relatively restrictive license.

Earlier versions of spaCy had an extension, [Neuralcoref](https://github.com/huggingface/neuralcoref), that was excellent but that was never made publicly available for any language other than English. The aim of Coreferee, on the other hand, is to get coreference resolution working for a variety of languages: our focus is less on necessarily achieving the best possible precision and recall for English than on enabling the functionality to be reproduced for new languages as easily and as quickly as possible. Because training data is in such short supply for most languages and is very effort-intensive to produce, it is important to use what is available as effectively as possible.

There are three essential strategies that human readers employ to recognise coreferences within a text:

1. Hard grammatical rules that completely preclude entities within a text from coreferring, e.g. _**The house** stood tall. **They** went on walking._ Such rules play an especially important role in languages that have grammatical gender, which includes most continental European languages.

2. Pragmatic tendencies, e.g. a word that begins a sentence and that is a grammatical subject is more likely than a word that is in the middle of a sentence and that forms part of a prepositional phrase to be referred back to by a pronoun that follows it in the next sentence.

3. Semantic restrictions, i.e. which entities can realistically do what to which entities in the world being described. For example, in the sentence _The child saddled **her** up_, a reader's experience of the world will make it clear that _her_ must refer to a horse.

With unlimited training data, it would be possible to train a system to employ all three strategies effectively from first principles using word vectors. The features of Coreferee that allow effective learning with the limited training data that is available are:

- Strategy 1) is covered by hardcoded rules for each language that the system is then not required to learn from the training data. Because detailed knowledge of the grammar of a specific natural language is a separate skill set from knowledge of machine learning, the two concerns have been fully separated in Coreferee: rules are covered in a separate module from tendencies. This means that a model for a new language can be generated by a competent Python programmer with no knowledge of machine learning or neural networks;

- Because the pragmatic tendencies for strategy 2) are very complex and only partially understood by linguists, machine learning and neural networks represent the only realistic way of tackling them. In order to reduce the amount of training data required for neural networks to learn effectively, the syntactic and morphological information supplied by the spaCy models, which have typically been trained with considerably more training data than will be available for coreference resolution, is used as input to neural networks alongside the standard [word vectors](#the-neural-ensemble).

- Especially with limited training data but probably even with the largest available training datasets, it is unlikely that a system will learn more than the very simplest tendencies for strategy 3). However, making word vectors available to neural networks ensures that Coreferee can make use of whatever tendencies are discernable.

Coreferee started life to assist the [Holmes](https://github.com/explosion/holmes-extractor) project, which is used for information extraction and intelligent search. Coreferee is in no way dependent on Holmes, but this original aim has led to several design decisions that may seem somewhat atypical. Several of them could easily be altered by someone with a requirement to do so:

- A mention within Coreferee does not consist of a span, but rather of a single token or of a list of tokens that stand in a coordination relationship to one another.

- Coreferee does not capture coreferences that are unambiguously evident from the structure of a sentence. For example, the identity of _he_ and _doctor_ in the sentence _**He** was a **doctor**_ is not reported by Coreferee because it can easily be derived from a simple analysis of the copular structure of the phrase.

- Repetitions of first- and second-person pronouns (_**I** was tired. **I** went home_) are not captured as they add no value either for information extraction or for intelligent search.

- Coreferee focusses heavily on anaphors (for English: pronouns). There is only relatively limited capture of coreference between noun phrases, and it is entirely rule-based. (In turn, however, this serves the aim of working with limited training data: noun-phrase coreference is a more exacting task than anaphor resolution.)

- Because search performance is much more important for Holmes than document parsing performance, Coreferee performs all analysis eagerly as each document passes through the pipe.

<a id="facts-and-figures"></a>

#### 1.4 Facts and figures

<a id="covered-relevant-linguistic-features"></a>

##### 1.4.1 Covered relevant linguistic features

<table style="text-align:center; vertical-align:middle">
  <tr><td rowspan="2">ISO 639-1</td><td rowspan="2">Language</td><td colspan="3">Anaphor expression</td><td rowspan="2">Agreement classes</td><td colspan="2">Coordination expression</td></tr><tr><td align="center">Pronominal</td><td align="center">Verbal</td><td align="center">Prepositional</td><td align="center">Conjunctive</td><td align="center">Comitative</td></tr>
  <tr><td align="center">en</td><td align="center">English</td><td align="center"><i><b>My friend</b> came in. <b>He</b> was happy.</i><td align="center">-</td><td align="center">-</td><td align="center">Three singular (natural genders) and one plural class.</td><td align="center"><i><b>Peter and Mary</b></i></td><td align="center">-</td></tr>
  <tr><td align="center">de</td><td align="center">German</td><td align="center"><i><b>Mein Freund</b> kam rein. <b>Er</b> war glücklich.</i><td align="center">-</td><td align="center"><i>Ich benutzte <b>das Auto</b> und hatte <b>damit</b> einige Probleme.</i></td><td align="center">Three singular (grammatical genders) and one plural class.</td><td align="center"><i><b>Peter und Maria</b></i></td><td align="center">-</td></tr>
  <tr><td align="center">fr</td><td align="center">French</td><td align="center"><i><b>Mon ami</b> entra. <b>Il</b> était heureux.</i><td align="center">-</td><td align="center">-</td><td align="center">Two singular (grammatical genders) and two plural (grammatical genders) classes.</td><td align="center"><i><b>Pierre et Marie</b></i></td><td align="center">-</td></tr>
   <tr><td align="center">pl</td><td align="center">Polish</td><td align="center"><i>Wszedł <b>mój kolega</b>. Widzieliście, jaki <b>on</b> był szczęśliwy?</i><td align="center"><i>Wszedł <b>mój kolega</b>. Szczęśliwy <b>był</b>.<sup>1</sup></i></td><td align="center">-<sup>2</sup></td><td align="center">Three singular (grammatical genders) and two plural (natural genders) classes.</td><td align="center"><i><b>Piotr i Kasia</b></i></td><td align="center">1) <i><b>Piotr z Kasią</b> przyjechali do Warszawy</i>; <br>2)&nbsp;<i>Widziałem Piotra i <b>przyszli z Kasią</i></b></td></tr>
  </table>

1. Only subject zero anaphors are covered. Object zero anaphors, e.g. <i>Wypiłeś <b>wodę</b>? Tak, <b>wypiłem.</b></i> are not in scope because they are mainly used colloquially and do not normally occur in the types of text for which [Coreferee is primarily designed](#background-information). Handling them would require creating or locating a detailed dictionary of verb valencies.

2. Polish has a restricted use of anaphoric prepositions in some formal registers, e.g. _Skończyło się to **dlań** smutno_. Because the Polish spaCy models were trained on news texts, they do not recognise such prepositions, meaning that Coreferee cannot capture them either.

<a id="model-performance"></a>

##### 1.4.2 Model performance

<table style="text-align:center; vertical-align:middle">
  <tr><td rowspan="2">ISO 639-1</td><td rowspan="2">Language</td><td rowspan="2">Training corpora</td><td rowspan="2">Total words in training corpora</td><td colspan="2"><code>*_trf</code> models</td><td colspan="2"><code>*_lg</code> models</td><td colspan="2"><code>*_md</code> models</td><td colspan="2"><code>*_sm</code> models</td></tr>  
  <tr><td align="center">Anaphors in 20%</td><td align="center">Accuracy (%)</td><td align="center">Anaphors in 20%</td><td align="center">Accuracy (%)</td><td align="center">Anaphors in 20%</td><td align="center">Accuracy (%)</td><td align="center">Anaphors in 20%</td><td align="center">Accuracy (%)</td></tr>
  <tr><td align="center">en</td><td align="center">English</td><td align="center"><a href="https://opus.nlpl.eu/ParCor/">ParCor</a>/<a href="https://github.com/dbamman/litbank"> LitBank</a></td><td align="center">393564</td><td align="center"><b>2500—2520</b></td><td align="center"><b>82—83</b><td align="center"><b>2480—2520</b></td><td align="center"><b>81—82</b></td></td><td align="center">2480—2510</td><td align="center">81</td><td align="center">2540—2560</td><td align="center">81—82</td></tr>
  <tr><td align="center">de</td><td align="center">German</td><td align="center"><a href="https://opus.nlpl.eu/ParCor/">ParCor</a></td><td align="center">164300</td><td align="center">-</td><td align="center">-</td><td align="center"><b>530—570</b></td><td align="center"><b>79—80</b></td><td align="center">520—550</td><td align="center">79—80</td><td align="center">530—550</td><td align="center">76—79</td></tr>
  <tr><td align="center">fr</td><td align="center">French</td><td align="center"><a href="https://www.ortolang.fr/market/corpora/democrat/v1.1">DEMOCRAT</a></td><td align="center">323754</td><td align="center">-</td><td align="center">-</td><td align="center"><b>1270—1280</b></td><td align="center"><b>71—72</b></td><td align="center">1280—1300</td><td align="center">68—70</td><td align="center">1130—1140</td><td align="center">63—64</td></tr>
  <tr><td align="center">pl</td><td align="center">Polish</td><td align="center"><a href="http://zil.ipipan.waw.pl/PolishCoreferenceCorpus">PCC</a></td><td align="center">548268</td><td align="center">-</td><td align="center">-</td><td align="center"><b>1730—1790</b></td><td align="center"><b>72—76</b></td><td align="center">1750—1790</td><td align="center">70—75</td><td align="center">-</td><td align="center">-</td></tr>
</table>

Coreferee produces a range of neural-network models for each language corresponding to the various spaCy models for that language. The [neural network inputs](#the-neural-ensemble) include word vectors. With `_sm` (small) models, both spaCy and Coreferee use context-sensitive tensors as an alternative to word vectors. `_trf` (transformer-based) models, on the other hand, do not use or offer word vectors at all. To remedy this problem, the model configuration files (`config.cfg` in the directory for each language) allow a **vectors model** to be specified for use when a main model does not have its own vectors. Coreferee then combines the linguistic information generated by the main model with vector information returned for the individual words in each document by the vectors model.

Because the Coreferee models are rather large (20GB-30GB for the group of models for a given language) and because many users will only be interested in one language, the group of models for a given language is installed using `python3 -m coreferee install` as demonstrated in the introduction. All Coreferee models are more or less the same size; a larger spaCy model does not equate to a larger Coreferee model. As the figures above demonstrate, the accuracy of Coreferee corresponds closely to the size of the underlying spaCy model, and users are urged to use the larger spaCy models. It is in any case unclear whether there is a situation in which it would make sense to use Coreferee with an `_sm` model as the Coreferee model would then be considerably larger than the spaCy model! As this discrepancy is especially extreme for the Polish models, Coreferee no longer supports `pl_core_news_sm` from version 1.1.0 onwards.

The English, German and Polish models support spaCy versions from 3.0.0 to 3.3.0, while the French models support spaCy versions from 3.1.0 to 3.2.0. Because the accuracies and number of anaphors found differ slightly depending on the spaCy version used, the table above cites ranges for each model.

Assessing and comparing the precision and recall of anaphor resolution algorithms is notoriously difficult. For one thing, two human annotators of the same data will not always agree (and, indeed, there are some cases where Coreferee and a training annotator disagree where Coreferee's interpretation seems the more plausible!) And the same algorithm may perform with wildly different accuracies with different test documents depending on how clearly the documents are written and how often there are competing interpretations of individual anaphors.

Because Coreferee decides where there are anaphors to resolve (as opposed to what to resolve them to) in a purely rule-based fashion and because there is not necessarily a perfect correspondence between the types of anaphor these rules are aiming to capture and the types of anaphor covered by any given training corpus, a recall measure would not be meaningful. Instead, we compare the performance between spaCy models — and, during tuning, between different hyperparameter values — by counting the total **number of anaphors** that the rules find within the test documents as parsed by the spaCy model being used and that are also annotated with a coreference within the training data. The **accuracy** then expresses the percentage of these anaphors for which the coreference annotated by the corpus author is part of the chain(s) suggested by Coreferee. In situations where the training data specifies a chain C->B->A and B is a type of coreference that Coreferee is not aiming to capture, C->A is used as a valid training reference.

The corpus for each language is split up into a training corpus (around 80%) and a test corpus (around 20%) using a random procedure with a constant seed, meaning that both sets contain documents from throughout each corpus and that the same documents end up in each set on all runs. Note that the corpora were not split up in this way prior to version 1.2.0, meaning that accuracy figures obtained for earlier versions are not directly comparable with accuracy figures obtained for subsequent versions.

Since coreference between noun phrases is restricted to a small number of cases captured by [simple rules](#noun-pair-detection), the model assessment figures presented here refer solely to [anaphor resolution](#anaphor-pair-analysis). When anaphor resolution accuracy is being assessed for a test document, noun pairs are detected and [added to chains](#building-the-chains) according to the standard rules, but they do not feature in the accuracy figures. On some rare occasions, however, they may have an indirect effect on accuracy by affecting the semantic considerations that determine which anaphors can be added to which chains.

Note that **Total words in training corpora** in the table above refers to 100% of the available data for each language, while the **Anaphors in 20%** columns specify the number of anaphors found in the roughly 20% of this data that is used for model assessment.

<a id="interacting-with-the-data-model"></a>

### 2 Interacting with the data model

Coreferee generates **Chain** objects where each chain is an ordered collection of **Mention** objects that have been analysed as referring to the same entity. Each mention holds references to one or more spaCy token indexes; a chain can have a maximum of one mention with more than one token (most often its leftmost mention). A given token index occurs in a maximum of two mentions; if it belongs to two mentions the mentions will belong to different chains and one of the mentions will contain multiple tokens. All chains that refer to a given `Doc` or `Token` object are managed on a `ChainHolder` object which is accessed via `._.coref_chains`. Reproducing part of the example from the [introduction](#getting-started-en):

```
>>> doc = nlp("Although he was very busy with his work, Peter had had enough of it. He and his wife decided they needed a holiday. They travelled to Spain because they loved the country very much.")
>>>
>>> doc._.coref_chains.print()
0: he(1), his(6), Peter(9), He(16), his(18)
1: work(7), it(14)
2: [He(16); wife(19)], they(21), They(26), they(31)
3: Spain(29), country(34)
>>>
>>> doc[16]._.coref_chains.print()
0: he(1), his(6), Peter(9), He(16), his(18)
2: [He(16); wife(19)], they(21), They(26), they(31)
>>>
```

Chains and mentions can be navigated much as if they were lists:

```
>>> len(doc._.coref_chains)
4
>>> doc._.coref_chains[1].pretty_representation
'1: work(7), it(14)'
>>> len(doc._.coref_chains[1])
2
>>> doc._.coref_chains[1][1]
[14]
>>> len(doc._.coref_chains[1][1])
1
>>> doc._.coref_chains[1][1][0]
14
>>>
>>> for chain in doc._.coref_chains:
...     for mention in chain:
...             print(mention)
...
[1]
[6]
[9]
[16]
[18]
[7]
[14]
[16, 19]
[21]
[26]
[31]
[29]
[34]
>>>
```

A document with Coreferee annotations can be saved and loaded using the normal spaCy methods: the annotations survive the serialization and deserialization. To facilitate this, Coreferee does not store references to spaCy objects, but merely to token indexes. However, each class has a pretty representation designed for human consumption that contains information from the spaCy document and that is generated eagerly when the object is first instantiated. Additionally, the `ChainHolder` object has a `print()` method that prints its chains' pretty representations with one chain on each line:

```
>>> doc._.coref_chains
[0: [1], [6], [9], [16], [18], 1: [7], [14], 2: [16, 19], [21], [26], [31], 3: [29], [34]]
>>> doc._.coref_chains.pretty_representation
'0: he(1), his(6), Peter(9), He(16), his(18); 1: work(7), it(14); 2: [He(16); wife(19)], they(21), They(26), they(31); 3: Spain(29), country(34)'
>>> doc._.coref_chains.print()
0: he(1), his(6), Peter(9), He(16), his(18)
1: work(7), it(14)
2: [He(16); wife(19)], they(21), They(26), they(31)
3: Spain(29), country(34)
>>>
>>> doc._.coref_chains[0]
0: [1], [6], [9], [16], [18]
>>> doc._.coref_chains[0].pretty_representation
'0: he(1), his(6), Peter(9), He(16), his(18)'
>>>
>>> doc._.coref_chains[0][0]
[1]
>>> doc._.coref_chains[0][0].pretty_representation
'he(1)'
>>>
```

Each chain has an index number that is unique within the document. It is displayed in the representations of `Chain` and `ChainHolder` and can also be accessed directly:

```
>>> doc._.coref_chains[2].index
2
```

Each chain can also return the index number of the mention within it that is **most specific**: noun phrases are more specific than anaphors and proper names more specific than common nouns:

```
>>> doc = nlp("He went to Spain. He loved the country. He often told his friends about it.")
>>> doc._.coref_chains.print()
0: He(0), He(5), He(10), his(13)
1: Spain(3), country(8), it(16)
>>>
>>> doc._.coref_chains[1].most_specific_mention_index
0
>>> doc._.coref_chains[1][doc._.coref_chains[1].most_specific_mention_index].pretty_representation
'Spain(3)'
```

This information is used as the basis for the `resolve()` method shown in the [initial example](#getting-started-en): the method traverses multiple chains to find the most specific mention or mentions within the text that describe a given anaphor or noun phrase head.

Note that a mention that heads a complex proper noun phrase only refers to the head of that phrase. Some users have expressed a requirement to retrieve all the tokens in such a phrase. Although this functionality is regarded as outside the main scope of Coreferee and is hence not available via the main data model, the information can be retrieved as follows:

```
rules_analyzer = nlp_en.get_pipe('coreferee').annotator.rules_analyzer
rules_analyzer.get_propn_subtree(doc[1])
```

<a id="how-it-works"></a>

### 3 How it works

<a id="general-operation-and-rules"></a>

#### 3.1 General operation and rules

<a id="anaphor-pair-analysis"></a>

##### 3.1.1 Anaphor pair analysis

For each language, methods are implemented that determine:

- for each token, its dependent siblings, e.g. _Jane_ is a dependent sibling of _Peter_ in the phrase _Peter and Jane_;
- for each token, whether the token is an anaphor (broadly speaking for English: a third-person pronoun);
- for each token, whether the token heads an independent noun phrase that an anaphor could refer to;
- for any independent-noun/anaphor or anaphor/anaphor pair within a text, whether or not semantic and syntactic constraints would permit coreference between the members of the pair. For example, there are no circumstances in which `they` and `her` could ever corefer within a text. When an entity has dependent siblings, the method is called twice, once with and once without the siblings. Possible coreferents are considered up to five sentences away from each anaphor looking backwards through the text. The method returns `2` (coreference permitted), `1` (coreference unlikely but possible) or `0` (coreference impossible). Alongside the language-specific rules, there are a number of language-independent rules which can lead to a `1` rather than a `2` analysis.

Each anaphor in a document emerges from an analysis using these methods with a list of elements to which it could conceivably refer. The list for each anaphor is scored using the [neural ensemble](#the-neural-ensemble) and the possible referents are ordered by decreasing likelihood. Regardless of their neural ensemble score, any pairs with the rules analysis `1` (coreference unlikely but possible) are ordered behind pairs with the rules analysis `2` (coreference permitted).

Note that anaphora is understood in a broad sense that includes cataphora, i.e. pronouns that refer forwards rather than backwards like the initial pronoun in the English example in the [introduction](#getting-started-en). Language-independent rules are used to determine situations in which the syntactic relationship between two elements within the same sentence permits cataphora.

Replacing the neural ensemble scoring with a naive algorithm that always selects the closest potential referent for each anaphor with rules analysis `2` (or `1` if there is no `2`) yields an accuracy of around 60% as opposed to the 84% reported [above](#model-performance). This demonstrates the respective contribution of each processing strategy to the overall result and provides a useful benchmark for any further machine learning experiments.

<a id="noun-pair-detection"></a>

##### 3.1.2 Noun pair detection

For each language the following are implemented:

- a method that determines whether a noun phrase is indefinite, or, in languages that do not mark indefiniteness, whether it could be interpreted as being indefinite;
- a method that determines whether a noun phrase is definite, or, in languages that do not mark definiteness, whether it could be interpreted as being definite;
- a dictionary from named entity labels to common nouns that refer to members of each named entity class. For example, the English named entity class `ORG` maps to the nouns `['company', 'firm', 'organisation']`.

This information is used in a purely rule-based fashion to determine probable coreference between pairs of noun phrases: broadly, definite noun phrases that do not contain additional new information refer back to indefinite or definite noun phrases with the same head word, and named entities are referred back to by the common nouns that describe their classes. Noun pairs can be a maximum of two sentences apart as opposed to the five sentences that apply to anaphoric references.

<a id="building-the-chains"></a>

##### 3.1.3 Building the chains

Coreferee goes through each document in natural reading order from left to right building up chains of anaphors and independent noun phrases. For each anaphor, the highest scoring interpretation as suggested by the neural ensemble is preferred. However, because the semantic (but not the syntactic) restrictions on anaphoric reference apply between all pairs formed by members of a chain rather than merely between adjacent members, it may turn out that the highest scoring interpretation is not permissible because it would lead to a semantically inconsistent chain. The interpretation with the next highest score is then tried, and so on until no interpretations remain.

In the unusual situation that all suggested interpretations of a given anaphor have been found to be semantically impossible, it is likely that one of the interpretations of the preceding anaphors in the text was incorrect: authors do not normally use anaphors that do not refer to anything. Reading the text:

```
The woman looked down and saw Lesley. She stood up and greeted him.
```

most readers will initially understand `she` as referring to `Lesley`. Only when one reaches the end of the sentence does it become clear that Lesley must be a man and that `she` actually refers to `the woman`. A quick test shows that Coreferee is capable of handling such ambiguity:

```
>>> doc = nlp('The woman looked down and saw Lesley. She stood up and greeted her.')
>>> doc._.coref_chains.print()
0: woman(1), her(13)
1: Lesley(6), She(8)
>>>
>>> doc = nlp('The woman looked down and saw Lesley. She stood up and greeted him.')
>>> doc._.coref_chains.print()
0: woman(1), She(8)
1: Lesley(6), him(13)
```

This is achieved using a **rewind**: at a point in a text where no suitable interpretation can be found for an anaphor, alternative interpretations of preceding anaphors are investigated in an attempt to find an overall interpretation that fits.

<a id="the-neural-ensemble"></a>

#### 3.2 The neural ensemble

The likelihood scores for [anaphoric pairs](#anaphor-pair-analysis) are calculated using an ensemble of five identical multilayer perceptrons using a rectified linear activation in the input and hidden layers. Each of the five networks outputs a probability between 0 and 1 for a given potential anaphoric pair. These probabilities are then fed into a softmax layer that selects the best potential referent for each anaphor.

The inputs to each of the five networks consist of:

1. A **feature map** for each member of the pair. As the first step in training, Coreferee goes through the entire training corpus and notes all the relevant morphological and syntactic information that relevant tokens, their syntactic head tokens and their syntactic children can have. This information is stored with the neural ensemble for each model as a **feature table**. The feature map for a given token (or list of tokens) is a oneshot representation with respect to the feature table.

2. A **position map** for each member of the pair capturing such information as its position within its sentence and its depth within the dependency tree generated for its sentence.

3. **Vector squeezers** for each member of the pair and, where existent, for the syntactic head of each member of the pair. The input to a vector squeezer is the [vector or context-sensitive tensor](#model-performance) for the spaCy token in question. A vector squeezer consists of three neural layers and outputs a representation that is only three neurons wide and that is fed into the rest of the network within the same layer as the other, non-vector inputs.

4. A **compatibility map** capturing the relationship between the members of the pair. Alongside the distance separating them in words and in sentences, this includes the number of common features in their feature maps and the cosine similarity between their syntactic heads.

Using a vector squeezer has been consistently found to offer slightly better results either than feeding the full-width vectors into the network directly or than omitting them entirely. Possible intuitions that might explain this behaviour are: the reduced width forces the network to learn and attend to a constrained number of specific semantic features relevant to coreference resolution; and the reduced width limits the attention of the network on the raw vectors in a situation where the training data is insufficient to make effective use of them.

Perhaps somewhat unusually, when a vector is required to represent a coordinated phrase, the mean of the vectors of the individual coordinated tokens is used rather than the mean of the vectors of all the tokens in the coordinated span.

The structure shared by each of the five networks in the ensemble is shown in the attached diagram:

![Structure of an ensemble member](https://github.com/explosion/coreferee/blob/master/docs/nn_structure.png)

Training for all relevant spaCy models for a given language takes between one and two hours on a high-end laptop.

<a id="adding-support-for-a-new-language"></a>

### 4. Adding support for a new language

One of the main design goals of Coreferee was to make it easy to add support for further languages. The prerequisites are:

- you will need to know the grammar of the language you are adding well enough to make detailed decisions about which coreferences are normal, which are marginally possible and which are impossible;
- you will need to be able to program in Python.

You should **not** need to get involved in the details of the neural ensemble; Coreferee should do that for you.

The steps involved are:

1. Create a directory under `coreferee/lang/` with the same structure as the existing language-specific directories; it is probably easiest to copy one of them.

2. The file `config.cfg` lists the spaCy models for which you wish to generate Coreferee models. You will need to specify a [separate vectors model](#model-performance) for any of the spaCy models that lack vectors or context-dependent tensors of their own — see the English `config.cfg` for an example. Each config entry specifies a minimum (`from_version`) and maximum (`to_version`) spaCy model version number that the generated Coreferee model will support, as well as the spaCy model version number with which the Coreferee model is trained (`train_version`). During development, all three numbers will normally refer to a single version number. Later, when an updated spaCy model version is brought out, testing will be required to see whether the existing Coreferee model still supports the new spaCy model version. If so, the maximum version number can be increased; if not, a new config entry will be necessary to accommodate the new Coreferee model that will then be required.

3. The file `rules.py` in the main code directory contains an abstract class `RulesAnalyzer` that must be implemented by a class `LanguageSpecificRulesAnalyzer` within a file called `language_specific_rules.py` in each language-specific directory. The abstract class `RulesAnalyzer` contains docstrings that specify for each abstract property and method the contract to which implementing classes should adhere. Looking at the existing language-specific rules is also likely to be helpful. The method `is_potential_anaphor()` is normally the most work to create: here it is probably worth looking at the existing English method for languages with natural gender or at the existing German method for languages with grammatical gender. (Polish has an unusually complex gender system, so the Polish example is unlikely to be helpful even as a basis for working with other Slavonic languages.)

4. There are some situations where word lists can be helpful. If a list is placed in a file `<name>.dat` within the `data` directory under a language-specific directory, the contents will be automatically made available within the `LanguageSpecificRulesAnalyzer` for the language in question as a variable `self.<name>` that contains a list where each entry corresponds to a line from the file; comments with `#` are supported. If you use a word list, please ensure it can be published under the MIT license and give appropriate attribution within the language-specific directory in the `LICENSE` and, where appropriate, in a `COPYING` file.

5. Male and female names are managed on a cross-linguistic basis because there is no reason why one would not want e.g. a German female name to be recognised within an English text. Names are automatically made available to all `RulesAnalyzer` implementations as properties `self.male_names`, `self.female_names`, `self.exclusively_male_names` and `self.exclusively_female_names`. If you can locate a suitable names list for the language you are working on that is available under a suitable license, add the attribution to the `LICENSE` file under `common/` and merge your names into the two files. Please tidy up the result so that the files are free of duplicates and in alphabetical order.

6. Create a language-specific directory under `tests/` with a file `test_rules_<ISO 639-1>.py` to test the rules you have written in 3-5). Although one of the corresponding files for one of the existing languages is likely to be the best starting point, you should also be sure to test any extra features specific to the language you are working on. The test tooling is designed to run each test against all spaCy models specified in `config.cfg`. At this stage in development, you will need to add temporarily a parameter `add_coreferee=False` to the call to `get_nlps()` in the `setUp()` method. Otherwise, all tests will fail because the test tooling will attempt to add the as yet non-existent Coreferee model to the pipe.

7. Some tests may fail with one of the smaller spaCy models because it produces incorrect syntactic representations rather than because of any issue with your rule code. For such cases, a parameter `excluded_nlps` can be specified within a test method to prevent it from being executed with specific spaCy models.

8. Locate a training corpus or corpora. Again, you should make sure that the resulting models can be published under the MIT license. Add new loader class(es) for the corpus or corpora to the existing loader classes in the `train/loaders.py` file. Loader classes must implement the `GenericLoader` abstract class that is located at the top of this file. The job of a loader is to read a specific training corpus format and to create and annotate spaCy documents with coreferences marked within corpora of that format. All the data for a single training run should be placed in a single directory; if there are multiple types of training data loaded by different loaders, each loader will need to be able to recognise the data it is required to read by examining the names of the files within the directory. It is worth spending some time checking with `print()` statements that the loaders annotate as expected, otherwise the training step that follows has little chance of success!

9. You are now ready to begin training. The training command must be issued from the `coreferee/` root directory. Coreferee will place a zip file into `<log-dir>`. Alongside the accuracy for each model, the files in the zip file show the coreference chains produced for each test document as well as a list of incorrect annotations where the Coreferee interpretation differed from the one specified by the training corpus author — information that is invaluable for debugging and rules improvement. As an example, the training command for English is:

```
python3 -m coreferee train --lang en --loader ParCorLoader,LitBankANNLoader --data <training-data-dir> --log <log-dir>
```

10. Measure the performance of your model against older versions of spaCy and the corresponding spaCy models: create a virtual environment for each version of spaCy, and from it measure the performance against the standard test corpus using the `coreferee check` command, of which an example is:

```
python3 -m coreferee check --lang en --loader ParCorLoader,LitBankANNLoader --data <training-data-dir> --log <log-dir>
```

11. Once you are happy with your models, install them. The command must be issued from the `coreferee/` root directory, otherwise Coreferee will attempt to download the models from GitHub where they are not yet present:

```
python3 -m coreferee install <ISO 639-1>
```

12. Before you attempt any regression tests that involve running Coreferee as part of the spaCy pipe, you must remove the `add_coreferee=False` parameter you added above. A setup where the parameter is present in one test file but absent in the other test file will not work because the spaCy models are loaded once per test run.

13. Again using one of the existing languages as an starting point, create a `test_smoke_tests_<ISO 639-1>.py` file in your test directory. The smoke tests are designed to make sure that the basic features of Coreferee are working properly for the language in question and should also cover any features that have posed a particular challenge while developing the rules.

14. Format your `language_specific_rules.py` using `black`.

15. Go through the documentation (`README.md` and `SHORTREADME.md`) adding information about the new language wherever the supported languages are listed in some way.

16. Issue a pull request. We ask that you supply us with the zip file placed into `<log-dir>` in point 9. Because this will contain a considerable amount of raw information from the training corpora, it will normally be preferable from a licensing viewpoint to <a href="mailto:richard@explosion.ai">send it out of band</a> rather than attaching it to the pull request.

<a id="adding-support-for-a-custom-spaCy-model"></a>

### 5. Adding support for a custom spaCy model

If you are using a custom spaCy model, you should generate a corresponding custom Coreferee model. Use points 2), 8), 9) and 10) from the [preceding section](#adding-support-for-a-new-language) as a guide. If you do not have your own training data, you can use the [same training data](#model-performance) that was used to generate the standard Coreferee models.

The language-specific rules expect specific entity tags as 'magic values'. This is unfortunate but there is no obvious alternative solution because there is no way of knowing which entities a new tag might refer to. The best advice is to use the same entity tags in your custom model as are used in the standard spaCy models when referring to similar entity classes.

For many entity tags, the impact will be minimal if you cannot adhere to this, but what is crucial is that you use the `PERSON` and `PER` tags to refer to people in English and German respectively. If this is not possible, change the language-specific-rule code and reinstall Coreferee locally (`python -m pip install .` from the root directory).

<a id="version-history"></a>

#### 6 Version history

<a id="version-100"></a>

##### 6.1 Version 1.0.0

The initial open-source version.

<a id="version-101"></a>

##### 6.2 Version 1.0.1

- Fixing of a bug where already installed models were reinstalled from `site-packages` rather than the new model being pulled from GitHub.

<a id="version-110"></a>

##### 6.3 Version 1.1.0

- Upgrade to Python 3.9 and spaCy 3.1
- Fixing of minor issues in all three rule-sets
- Regeneration of all models
- Improvement of the Polish examples in [section 1.4.1](#covered-relevant-linguistic-features) to make them more pragmatically correct - many thanks to Małgorzata Styś for her valuable advice on this.

<a id="version-111"></a>

##### 6.4 Version 1.1.1

- Changed the dependencies to allow Coreferee to run on the Apple M1 chipset
- Sorted out a problem with the supported spaCy versions
- Improved some of the tests

<a id="version-112"></a>

##### 6.5 Version 1.1.2

- Added support for French, which was kindly supplied by [Pantalaymon](https://github.com/Pantalaymon)

<a id="version-113"></a>

##### 6.6 Version 1.1.3

- Updated French rules to new version, again supplied by [Pantalaymon](https://github.com/Pantalaymon)
- Fixed an endless-loop problem in `language_independent_is_anaphoric_pair()`

<a id="version-120"></a>

##### 6.7 Version 1.2.0

- Removed dependencies to TensorFlow and Keras, switching to Thinc as the neural network platform. Switching to Thinc has led to serialized models that are around 30% of the size of the old models, and has also allowed the old limitation to be removed where `nlp.pipe()` could not be called with `n_process > 1` with forked processes.
- Implemented a softmax layer to select the best potential referent for each anaphor as opposed to calculating independent scores for each pair.
- Added matrix tests to support a variety of Python and spaCy versions, including spaCy 3.2 and spaCy 3.3.
- Implemented a stable-random split into train and test corpora as opposed to using the last 20% of loaded documents as the test corpus.
- Improved the training script so that it remembers the model state at each epoch and chooses the best-performing state from the training history as the model to save.
- Added the `coreferee check` command to enable performance measurement for an existing Coreferee model with a new spaCy model.

<a id="open-issues"></a>

### 7. Open issues / requests for assistance

1. Because optimising parsing speed was not a priority in the [project within which Coreferee came into being](#background-information), Coreferee is written purely in Python; it would be helpful if somebody could convert relevant parts of it to Cython.

2. It would be useful if somebody could find a way of benchmarking Coreferee against other coreference resolution solutions, especially for English. One problem this would probably present is that using a benchmark necessitates a normative scope where a system aims to find exactly those types of coreference marked within the benchmark corpus, whereas the scope of Coreferee was determined by project requirements.
