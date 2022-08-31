# Inflector - pregibalnik

V tem repozitoriju se nahaja rezultat aktivnosti A3.1 - R1.3.2 Orodje za celovit jezikoslovni ročni pregled in popravljanje strojno pridobljenega leksikonskega gradiva, ki je nastalo v okviru projekta Razvoj slovenščine v digitalnem okolju.

---

This repository contains ... TODO

```
- parameter: buildx build --platform linux/amd64, for example:
    docker buildx build --platform linux/amd64 -t clarin/form-generator .

- accentuator error when running:
    accentuatorr_1  | 2022-08-31 15:34:22.032529: F tensorflow/core/lib/monitoring/sampler.cc:42] Check failed: bucket_limits_[i] > bucket_limits_[i - 1] (0 vs. 10)
    accentuatorr_1  | qemu: uncaught target signal 6 (Aborted) - core dumped

- v dokumentacijo vključiti tudi povezave za Swagger, npr. http://localhost:9091/docs (za posamezne in za glavni servis 9091, 9092, 9093, 9095)
    - sprogramirati tako, da bo že v Swaggerju na voljo en testni primerček
    - v navodilih mora biti definiran tudi format vhodov


- docker-compose:
    - dodati build namesto image, da se direktno zbilda (vsaj v glavnem docker compose-u)
    - dodati platform parameter
    - restart sem dal na always
    ---> glavni docker-compose je v root mapi in najbolje, da se ga lahko zažene z enim ukazom, kot je že pripravljeno

```

 ---

> Operacijo Razvoj slovenščine v digitalnem okolju sofinancirata Republika Slovenija in Evropska unija iz Evropskega sklada za regionalni razvoj. Operacija se izvaja v okviru Operativnega programa za izvajanje evropske kohezijske politike v obdobju 2014-2020.

![](Logo_EKP_sklad_za_regionalni_razvoj_SLO_slogan.jpg)