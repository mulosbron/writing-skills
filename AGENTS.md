# Writing Skills (Yazarlık & Kurgu Skilleri) Orkestrasyon Rehberi

Bu paket; **bilimsel/akademik, blog, metin yazarlığı, ortak belge ve editoryal düz yazı** (Türkçe/İngilizce/Çince) üretiminin yanı sıra, **uzun soluklu kurgu, roman, öykü, şiir, devamlılık (continuity) takibi ve yayıncılık** süreçleri için **54 skill** ve **10 kurgu alt-ajanı (`agents/`)** içerir.

İhtiyaca göre aşağıdaki iki ana iş akışından birini seçin:

---

## 🔄 İş Akışı A: Makale, Akademik, Deneme ve Düz Yazı

Uzun metinlerde skilleri sırayla zincirleyin; kısa metinlerde 2. aşamayı atlayabilir veya 3. ile 4. aşamayı birleştirebilirsiniz.

1. **Planlama ve İlk Taslak (Drafting)**
   - Bilimsel/Akademik: `scientific-writing`
   - Blog / Standart Makale: `blog-writing-guide`
   - Deneme (Essay): `crossframe-essay`
   - Genel İçerik: `content-writer-assistant`
   - Dönüşüm Odaklı Metin / E-posta & Açılış Sayfası: `copywriting`
   - Aşamalı Ortak Belge Yazımı (Spec / PRD / Teklif): `doc-coauthoring`
   - Veri Anlatımı: `data-storytelling`
   - Teknik / Açıklayıcı Wiki: `wiki-page-writer`
2. **Üslup ve Akıcılık (Styling)**
   - Edebi dokunuş: `beautiful-prose`
   - LLM klişelerinden arındırılmış sade anlatım: `llm-writing`
3. **İnsansılaştırma (Humanizing)**
   - Türkçe metinler: `turkce-humanizer`
   - İngilizce metinler: `avoid-ai-writing` / `english-humanizer`
   - Çince metinler: `humanize-chinese`
   - CLI tabanlı deterministik AI kalıbı temizliği: `unslop`
4. **Editoryal Kontrol ve Son Okuma (Editing & Proofreading)**
   - Yapı & akış: `copy-editing`
   - Yazım, dilbilgisi ve noktalama: `professional-proofreader`

---

## 📖 İş Akışı B: Kurgu, Öykü ve Roman (Creative Writing + Story Bible)

Kurgu projelerinde ihtiyaca göre **Muse / Craft iş akışı** (`creative-writing-*`, `story-*`) veya **Markdown Story Bible / CLI süreklilik iş akışı** (`story-init`, `story-maintenance`, `revision-continuity`, vb.) birlikte kullanılabilir:

1. **Kurulum ve Fikir Geliştirme**
   - Proje & stil kurulumu: `project-setup` (kb/ ve stil dosyaları) veya `story-init` (YAML frontmatter tabanlı `story.md` / hikâye İncili)
   - Fikir & öncül testi: `premise-workshop`, `creative-writing-muse`, `story-planning`
   - Dünya & oyun kurgusu: `worldbuilding` (kurgu dünya, sihir/kültür/takvim/sözlük), `wordbuilding` (oyun dünyası kurgusu), `creative-research`, `research`
2. **Yapı, Karakter ve Taslak Yazımı**
   - Olay örgüsü, tema ve ses: `plot-structure`, `theme-craft`, `character-management`, `character-sim`, `voice-style`
   - Sahne & bölüm yazımı: `story-workflow`, `creative-writing-craft`, `discovery-drafting`, `scene-craft`, `chapter-writing`, `verse-craft`, `interactive-fiction`, `genre-craft`
   - Süreklilik & hafıza: `story-memory`, `series-continuity`, `story-maintenance`
3. **Okuma, Eleştiri, Revizyon ve Yayın**
   - Okuyucu & editoryal inceleme: `story-review`, `reader-sim`, `reader-panel`, `editorial-review`, `feedback-triage`, `writing-staffing`
   - Çizgi/süreklilik revizyonu: `line-editing`, `revision-continuity`, `writing-principles`
   - Çeviri/uyarlama & basım: `adaptation`, `submission`, `publishing`

Kurgu alt-ajan rolleri (`agents/`): `muse`, `brainstormer`, `outliner`, `writer`, `style-creator`, `critic`, `continuity-checker`, `character-sim`, `reader-sim`, `creative-researcher`.

---

## 📚 Skill Envanteri (54 Skill)

### Düz Yazı, İnsansılaştırma & Editörlük (18)
| Skill | Yol | Amaç |
|---|---|---|
| `scientific-writing` | `skills/scientific-writing/SKILL.md` | Bilimsel ve akademik yazılar, kaynakça ve nesnellik. |
| `blog-writing-guide` | `skills/blog-writing-guide/SKILL.md` | Akıcı blog yazıları ve yapılandırılmış makaleler. |
| `crossframe-essay` | `skills/crossframe-essay/SKILL.md` | Derinlikli, argüman sunan deneme (essay) yazımı. |
| `data-storytelling` | `skills/data-storytelling/SKILL.md` | İstatistik ve verileri ikna edici anlatıya dönüştürme. |
| `content-writer-assistant` | `skills/content-writer-assistant/SKILL.md` | Genel içerik ve metin yazarlığı asistanlığı. |
| `copywriting` | `skills/copywriting/SKILL.md` | Açılış sayfaları ve e-postalar için uydurmasız, dönüşüm odaklı metin yazarlığı. |
| `doc-coauthoring` | `skills/doc-coauthoring/SKILL.md` | Bağlam toplama, yinelemeli yapılandırma ve okur testi ile ortak belge yazımı. |
| `wiki-page-writer` | `skills/wiki-page-writer/SKILL.md` | Nesnel wiki / ansiklopedi bilgi sayfaları. |
| `beautiful-prose` | `skills/beautiful-prose/SKILL.md` | Edebi, akıcı ve zengin üslup geliştirme. |
| `llm-writing` | `skills/llm-writing/SKILL.md` | Okur odaklı sade dil seçimi ve LLM kalıplarını temizleme. |
| `avoid-ai-writing` | `skills/avoid-ai-writing/SKILL.md` | İngilizce metinleri yapay zeka klişelerinden arındırma. |
| `unslop` | `skills/unslop/SKILL.md` | Yayın öncesi `unslop` CLI ile deterministik AI yazım kalıbı temizliği. |
| `turkce-humanizer` | `skills/turkce-humanizer/SKILL.md` | Türkçe metinleri doğal ve yerel hale getirme. |
| `english-humanizer` | `skills/english-humanizer/SKILL.md` | İngilizce metinleri insan eli değmiş gibi doğallaştırma. |
| `humanize-chinese` | `skills/humanize-chinese/SKILL.md` | Çince metinlerde AI izi tespiti, doğallaştırma ve akademik AIGC azaltımı. |
| `copy-editing` | `skills/copy-editing/SKILL.md` | Paragraf akışı, tutarlılık ve editoryal kurgu. |
| `professional-proofreader` | `skills/professional-proofreader/SKILL.md` | Yazım, noktalama ve dilbilgisi son kontrolü. |
| `wordbuilding` | `skills/wordbuilding/SKILL.md` | Oyun ve interaktif evrenler için dünya inşası metodolojisi. |

### Yaratıcı Yazarlık İş Akışı & Zanaat (12)
| Skill | Yol | Amaç |
|---|---|---|
| `creative-writing-muse` | `skills/creative-writing-muse/SKILL.md` | Hikâye geliştirme, yazma ve revizyonda ana yaratıcı ortak. |
| `story-workflow` | `skills/story-workflow/SKILL.md` | Niyet okuma, üretim, eleştiri ve onay döngüsü orkestrasyonu. |
| `project-setup` | `skills/project-setup/SKILL.md` | Hikâye projesi, `kb/` ve stil dosyaları ilk kurulumu. |
| `story-planning` | `skills/story-planning/SKILL.md` | Beyin fırtınası, yaratıcı yönelim ve hikâye mimarisi. |
| `story-memory` | `skills/story-memory/SKILL.md` | Gerçek/olay çıkarımı, bilgi tabanı düzeni ve süreklilik kaydı. |
| `creative-writing-craft` | `skills/creative-writing-craft/SKILL.md` | Sahne mekaniği, düz yazı modları, stil analizi ve tür zanaatı. |
| `creative-research` | `skills/creative-research/SKILL.md` | Tarihi, kültürel ve alana özgü kaynaklı kurgu araştırması. |
| `character-sim` | `skills/character-sim/SKILL.md` | Karakterin sesi, bilgisi ve ruh haliyle rol/diyalog simülasyonu. |
| `reader-sim` | `skills/reader-sim/SKILL.md` | İlk kez okuyan okur gözüyle anlık okuma tepkisi simülasyonu. |
| `story-review` | `skills/story-review/SKILL.md` | Gelişimsel edit, çizgi editi, düzyazı eleştirisi ve süreklilik denetimi. |
| `writing-principles` | `skills/writing-principles/SKILL.md` | Temel yazarlık ilkeleri, anti-kalıplar ve hata modları. |
| `writing-staffing` | `skills/writing-staffing/SKILL.md` | Üretici ve inceleyici ajan görev dağılım rehberi. |

### Kurgu Mühendisliği, Hikâye İncili & Yayıncılık (24)
| Skill | Yol | Amaç |
|---|---|---|
| `story-init` | `skills/story-init/SKILL.md` | Markdown + YAML frontmatter tabanlı hikâye projesi başlatma. |
| `premise-workshop` | `skills/premise-workshop/SKILL.md` | Hikâye fikri, biçim seçimi, logline ve premise testi. |
| `worldbuilding` | `skills/worldbuilding/SKILL.md` | Mekân, sihir/teknoloji, kültür, takvim ve isim dili inşası. |
| `character-management` | `skills/character-management/SKILL.md` | Karakter profilleri, ilişkiler, arc ve karakter durum takibi. |
| `plot-structure` | `skills/plot-structure/SKILL.md` | Olay örgüsü, MICE iplikleri, kısa öykü ve tempo planlama. |
| `theme-craft` | `skills/theme-craft/SKILL.md` | Tema, ana fikir, yalan/gerçek ve antagonist tematik ekseni. |
| `voice-style` | `skills/voice-style/SKILL.md` | Stil kılavuzu, ses parmak izi ve dil tutarlılığı kuralları. |
| `genre-craft` | `skills/genre-craft/SKILL.md` | Türlere özgü kurgu kuralları (gizem ipuçları, seri/bölümlü kurgu vb.). |
| `scene-craft` | `skills/scene-craft/SKILL.md` | Sahne amacı, çatışma, dönüm noktası ve geçiş kurgusu. |
| `chapter-writing` | `skills/chapter-writing/SKILL.md` | Sahne planlarından bölüm taslağı üretme rehberi. |
| `discovery-drafting` | `skills/discovery-drafting/SKILL.md` | Katı taslak olmadan keşifsel (pantsing) yazım ve sahne keşfi. |
| `verse-craft` | `skills/verse-craft/SKILL.md` | Şiir, vezin/ritim taraması, kafiye ve şarkı sözü yazımı. |
| `interactive-fiction` | `skills/interactive-fiction/SKILL.md` | Dallanan anlatı ve interaktif kurgu tasarımı. |
| `research` | `skills/research/SKILL.md` | Gerçek dünya doğrulamaları, uzman notları ve bölüm bağlantıları. |
| `revision-continuity` | `skills/revision-continuity/SKILL.md` | Ölü karakter, zaman çizelgesi ve kurulum-karşılık süreklilik kontrolü. |
| `line-editing` | `skills/line-editing/SKILL.md` | Cümle ritmi, diyalog sesi ve satır düzeyinde inceltme. |
| `reader-panel` | `skills/reader-panel/SKILL.md` | Çoklu beta-okur paneli ve perspektif raporlaması. |
| `feedback-triage` | `skills/feedback-triage/SKILL.md` | Okur/editör geri bildirimlerini sınıflandırma ve revizyon planlama (`templates/`). |
| `editorial-review` | `skills/editorial-review/SKILL.md` | İzinler, işbirliği ve editoryal inceleme süreçleri (`templates/`). |
| `series-continuity` | `skills/series-continuity/SKILL.md` | Çok kitaplı serilerde seri İncili ve süreklilik yönetimi. |
| `adaptation` | `skills/adaptation/SKILL.md` | Çeviri, resimli kitap ve ortam uyarlama teknikleri. |
| `story-maintenance` | `skills/story-maintenance/SKILL.md` | Story CLI doğrulama, indeks onarımı, dışa aktarım ve diyagram üretimi. |
| `submission` | `skills/submission/SKILL.md` | Sorgu mektubu (query), tanıtım yazısı (blurb) ve dergi/ajans başvuruları. |
| `publishing` | `skills/publishing/SKILL.md` | Bağımsız yayıncılık üretimi, meta veri ve hak anlaşmaları. |

## Sınırlar

- Okunacak/yazılacak dosyaların kendi diline ve proje konvansiyonlarına uyun; Türkçe metinlere İngilizce kalıp, mevcut bir hikâye İncili'ne (`kb/` veya `story.md`) uymayan kanon icadı eklemeyin.
- Yazar onaylamadan yayımlanmış/kesinleşmiş (`final`) bölümlerin kanon kararlarını sessizce değiştirmeyin.
