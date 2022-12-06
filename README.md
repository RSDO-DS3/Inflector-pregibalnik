# Inflector - pregibalnik

V tem repozitoriju se nahaja rezultat aktivnosti A3.1 - R1.3.2 Orodje za celovit jezikoslovni ročni pregled in popravljanje strojno pridobljenega leksikonskega gradiva, ki je nastalo v okviru projekta Razvoj slovenščine v digitalnem okolju.

---

This repository contains the code for Pregibalnik (Inflector), a piece of software consisting of three components: the form generator, the accentuator, and the phonetic converter. Words in Slovene are inflected for different grammatical categories such as case, person, number and gender, and the main goal of the Inflector is to take a (Slovene) lemma and its lexical features (e.g. "eholokacija", noun, common, feminine) as the input and provide all of its inflected forms (e.g. "eholokacija", "eholokacije", "eholokaciji", ...), their accentuated forms ("eholokácija", "eholokácije", "eholokáciji", ...), and their phonetic transcriptions in IPA ("ɛxɔlɔˈkaːʦija", "ɛxɔlɔˈkaːʦijɛ", "ɛxɔlɔˈkaːʦiji", ...) and SAMPA ('ExOlO"ka:tsija', 'ExOlO"ka:tsijE', 'ExOlO"ka:tsiji').

The form generator generates forms according to morphological patterns predicted by logistic regression models. The accentuator assigns accents to these forms using neural networks (see Krsnik 2017; Gitea: https://gitea.cjvt.si/lkrsnik/stress_asignment). The phonetic converter is rule-based.

Pregibalnik takes the lemma and its lexical features or its morphosyntactic tag (e.g. "eholokacija", "Sozei"; according to the Multext-East v6 system: http://nl.ijs.si/ME/V6/msd/html/msd-sl.html#msd.msds-sl) and returns a .JSON file with all the above-mentioned forms (see "output_example_Som-naftaš.json" for more details).


To deploy Pregibalnik (Inflector) clone the git repository. Copy `docker-compose.base-example.yaml` to `docker-compose.yaml` and if neccessary edit according to your local configuration needs (volume locations, ports). Build the Docker image with `docker-compose build`. 

Run the containers with `docker-compose up -d`. The Pregibalnik (Inflector) API will be accessible at `http://127.0.0.1:5015` (by default configured on port 5015, limited to localhost; edit `docker-compose.yaml` to change). Component APIs are accessible on ports defined in `docker-compose.yaml`.

Swagger documentation is available at `http://localhost:5015/docs` and `http://localhost:5015/redoc`. Component APIs are accessible in similar manner on their respective ports.
Check for errors with `docker logs`.

For deployments behind reverse proxy (e.g. _Nginx_) see `docker-compose.base-example.yaml`. Modify `API_ROOT_PATH` according to your needs. The example shows deployment `example-server.org/pregibalnik` as the main API endpoint and `example-server.org/pregibalnik/form-generator` etc. for the components. Swagger documentation is accessible at `example-server.org/pregibalnik/docs`, `example-server.org/pregibalnik/form-generator/docs` etc.


---

> Operacijo Razvoj slovenščine v digitalnem okolju sofinancirata Republika Slovenija in Evropska unija iz Evropskega sklada za regionalni razvoj. Operacija se izvaja v okviru Operativnega programa za izvajanje evropske kohezijske politike v obdobju 2014-2020.

![](Logo_EKP_sklad_za_regionalni_razvoj_SLO_slogan.jpg)
