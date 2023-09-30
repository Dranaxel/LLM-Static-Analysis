# LLM Static analysis

This project aims to create a CLI allowing static analysis on files to get recommandations

## Exemple

```
└─(00:00:00 on main ✭)──> python main.py py /home/alexandre/Development/gpt-statis-analysis                                                              
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Filename                                                ┃ Code Quality ┃ Good Points                                    ┃ Bad Points                  ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ /home/alexandre/Development/gpt-statis-analysis/main.py │ 6            │ Use of Typer library for CLI                   │ Lack of comments            │
│                                                         │              │ Use of async/await for asynchronous operations │ Unclear variable names      │
├─────────────────────────────────────────────────────────┼──────────────┼────────────────────────────────────────────────┼─────────────────────────────┤
│ chain.py                                                │ 8            │ Efficient algorithms                           │ Lack of comments            │
│                                                         │              │ Effective use of data structures               │ Inefficient data structures │
│                                                         │              │ Thorough and constructive review criteria      │                             │
│                                                         │              │ Proper use of logging                          │                             │
└─────────────────────────────────────────────────────────┴──────────────┴────────────────────────────────────────────────┴─────────────────────────────┘
```

## How to use ?

if you use pipenv: `pipenv install`
otherwise: `pip install -r requirements.txt`

It actually woks only with openai gpt3, so you need to export your Openai api key via OPENAI_API_KEY

The cli is powered by the awesome [Typer](https://typer.tiangolo.com/) so it should be pretty self explainatory: `python main.py --help`
```
 Usage: main.py [OPTIONS] REGEXP PATH                                                                                                                                                                                
                                                                                                                                                                                                                     
╭─ Arguments ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    regexp      TEXT  [default: None] [required]                                                                                                                                                                 │
│ *    path        TEXT  [default: None] [required]                                                                                                                                                                 │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --help          Show this message and exit.                                                                                                                                                                       │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

for logs you can activate them with `LOGLEVEL=DEBUG` environment variable

# ToDo

[] Use HF LLM
[] Add onefile mode
[] Allow embedings from... ?
[] Add action like 'tests' or 'global analysis'
