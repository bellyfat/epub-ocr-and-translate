# epub-ocr-and-translate

### An in-progress set of tools for creating epubs in multiple languages

Scripts to scan a PDF, auto-translate, process, and create epub and PDF output...these scripts are quick and dirty: YMMV, use at your own risk, etc. etc.

**Dependencies:**
- python 2.7 (non-built-in modules used include: google.cloud guess_language pycountry)
- ImageMagick
- poppler-utils
- tesseract
- For translation, Google Translate API (with GOOGLE\_APPLICATION\_CREDENTIALS in your env) and Python module or [translate-shell](https://github.com/soimort/translate-shell). 
- texlive with xetex: Recommend installing the entire CTAN distribution (i.e., not using yum or apt-get but using the instructions from https://www.tug.org/texlive/quickinstall.html) and do this *before* installing pandoc
- pandoc
- ebook-viewer (optional; to view output)
- For LaTeX, applicable language packs (for example, you'll need to `sudo apt install texlive-lang-cyrillic` for russian, `texlive-lang-spanish` for Spanish, etc)

### Quick summary:

1. OCR a PDF with `ocr.sh`

    Given a PDF file, OCR and clean it up a little. Requires ImageMagick, tesseract, pdfinfo/pdfseparate. 

    **Usage**: 

    `sh ocr.sh filename.pdf eng`

    where `eng` is the three letter language code of the source document. See list [here](http://www.loc.gov/standards/iso639-2/php/code_list.php). Source language document is very important! Note that this may take awhile, depending on the number of pages in your PDF. 

2. Translate a file with `trans.py`

    `trans.py` uses Google's Translate API, which costs $ or [`translate-shell`](https://github.com/soimort/translate-shell), which is awesome, but you can and will get blocked by translation engines, so it's not great for large texts (but you *can* specify google, bing, yandex, etc). WARNING! translate-shell with many of the engines, even Google, can be unreliable because engines WILL block you after a certain number of characters. For important work, Google Cloud API is still unfortunately your best bet, though pricey, like $10/million characters.

    **Usage for trans.py:** `python trans.py -i source_text_file -s two-letter-source_lang -t two-letter-target_lang [-e trans|gcloud] [-w wait_seconds]`


    -e is optional, uses translate-shell by default. There's a default two second wait between translation requests, you can change this with -w.

3. Cut files into individual markdown files for each chapter using **split.py**
   
    **Usage:** 
    
    `python split.py -i filename.txt -d CHAPTER` 
    
    (where CHAPTER is the chapter-delimiter; accepts UTF-8, so you can use other languages where necessary. For example, if your source text is Russian, you could use "Глава"). 

4. Edit markdown output as needed. This is probably the hardest part. Good luck! You may want to skip this and run the other steps to see how much more post-processing work you've got to do. 

5. Build a Makefile that will generate your epub and PDF files from your Markdown source with `makemake.py`

    Creates a make file that will output epub and PDF, gathering all *.md files in the current directory. Requires xetex and pandoc. And ebook-viewer if you want to pop open the output. You should only have to run this once; if you run it again at some point, make sure you've deleted all autogenerated *lang*md files created using step 6.

    **Usage:** `python makemake.py`

6. Create PDF and epub files using `extract.sh`

    **Usage:** `sh extract.sh two_letter_lang`

    `extract.sh` requires `print-lang.py`, which can also be used in standalone mode. It takes a master file that contains two languages, like:

        Это по русски

        This is in English

        Это по русски

        This is in English

    And exports the language you specify. Usage is ``python print-lang.py input_file two_letter_lang_code``
    
Will add examples in the future, but the EASIEST way to use this while it's in development is to do something like this:

    pip install google.cloud guess_language pycountry
    
    mkdir my_book_directory
    
    cp mypdf.pdf my_book_directory
    
    cd my_book_directory && git clone https://github.com/jenh/epub-ocr-and-translate.git
    
    ln -s epub-ocr-and-translate scripts
    
      (Just for ease of use when running stuff)
    
    ln -s epub-ocr-and-translate/templates templates
    
    sh scripts/ocr.sh mypdf.pdf eng
    
    python scripts/trans.py -i mypdf.txt -s en -t es -w 3
      (This is slow, but if you don't have a Google translate API key, works without blockage for about 12 hours. If you have an api key, use "-e gcloud")
    
    python scripts/split.py -i mypdf.txt-2lang.md -d CHAPTER
    
    python scripts/makemake.py
    
    vi variables.yaml
      (Set these the way you want, title, author, etc.)
    
    sh scripts/extract.sh es
      (where 'es' is the language you want to build for, leave blank if you skipped the translation step and only have one language; note also that you'll need to install the appropriate texlive package -- like `texlive-lang-spanish` or `texlive-lang-cyrillic` to switch languages.)

You may also want to install epubcheck if you're planning on kindlegenning your epub output; it chokes on a lot of special characters and doesn't provide useful errors, but epubcheck should find them for you.
