# IP Intelligence Tool

![Python](https://img.shields.io/badge/Python-3.x-blue)
![Tool](https://img.shields.io/badge/Type-IP_Intelligence-black)
![Status](https://img.shields.io/badge/Status-Active-green)

Python ile yazdığım basit bir IP / domain analiz aracı.

Verdiğin domain veya IP hakkında temel bilgiler toplar (ülke, ISP vs.) ve küçük bir yorum yapar.

---

## nasıl kullanılır

```bash id="7b6e9h"
python intel_tool.py -t example.com
```

veya direkt IP:

```bash id="6b2d3x"
python intel_tool.py -t 8.8.8.8
```

---

## ne yapıyor

* domain → IP çevirir
* IP hakkında bilgi çeker
* ülke, şehir, ISP gibi bilgileri gösterir
* basit risk analizi yapar

---

## örnek

```bash id="2w8a1k"
python intel_tool.py -t google.com
```

çıktı:

```id="9p3c2m"
IP          : 142.xxx.xxx.xxx
Country     : United States
ISP         : Google LLC
Assessment  : Büyük ihtimalle normal
```

---

## ekstra

ham veri görmek için:

```bash id="5f1n0s"
python intel_tool.py -t google.com --json
```

---

## not

öğrenmek için yaptım, rastgele IP'lere saçma sapan yüklenme 👍

---

github: https://github.com/dorukcodes
