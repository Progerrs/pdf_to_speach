import argparse
import os.path
import gtts.tts
import pdfplumber
from loguru import logger
from pathlib import Path
from gtts import gTTS


parser = argparse.ArgumentParser()
parser.add_argument('path', type=str, help='Path to file')  # Позиционны
parser.add_argument('-l', '--language', type=str, help="Choose language, for example 'en', or 'ru'", default='ru')
args = parser.parse_args()


def file_exists(file_path=args.path) -> str:
    expansions = {'.pdf'}
    if Path(file_path).is_file() and Path(file_path).suffix in expansions:
        logger.info('File exists')
        return 'File exists'
    else:
        logger.error(f'FileNotFoundError or File not in {expansions}')
        raise FileNotFoundError


def read_pdf_file(file_path=args.path) -> str:
    text = ''
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text()
    logger.info('Successfully extracted the text from the file')
    return text


def text_to_audio(text: str, language=args.language) -> gtts.tts.gTTS:
    audio = gTTS(text=text, lang=language, slow=False)
    logger.info('Successfully converted text to audio')
    return audio


def save(file: gtts.tts.gTTS) -> str:
    name = Path(args.path).stem
    file.save(os.path.join('audio', f'{name}.mp3'))
    logger.info(f'{name}.mp3 saved successfully!')
    return f'{name}.mp3 saved successfully!'


def main() -> int:
    file_exists()
    text = read_pdf_file()
    text.replace('\n', ' ')
    audio = text_to_audio(text)
    save(audio)
    return 0


if __name__ == '__main__':
    main()
