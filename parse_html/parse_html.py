
# coding: utf-8

# In[1]:


# imports libaries
import re 							# regular expression
import datetime 					# dates
from bs4 import BeautifulSoup		# HTML parsing


# In[2]:


# sets page names
css_name = 'jupn.css'
html_name = 'ff_analysis.html'
title_name = 'Just Fanfiction Statistics'

# sets current year
cdate = '1999-12-31'
cdate = str(datetime.datetime.now()).split()[0]
date = datetime.datetime.strptime(cdate, '%Y-%m-%d')
date = date.strftime('%d %b %Y')


# In[3]:


# gets content page
content = open('story_analysis.html', 'r')
content_soup = BeautifulSoup(content, 'html.parser')
content.close()


# In[4]:


# gets css of content page
style = ''
for style_block in content_soup.find_all('style'):
    style = style + style_block.text + '\n'
    
# removes outer grey border from css
regex1 = re.compile(r'-webkit-box-shadow:.*;\n')
regex2 = re.compile(r'box-shadow:.*;\n')
style = re.sub(regex1, '', style)
style = re.sub(regex2, '', style)

# removes override
comment = '/* Overrides'
style = style.partition(comment)[0]

# remove margins
regex1 = re.compile(r'margin-left:.*;\n')
regex2 = re.compile(r'margin-right:.*;\n')
style = re.sub(regex1, '', style)
style = re.sub(regex2, '', style)


# In[5]:


# gets body of content page
body = content_soup.find('body')

# removes input boxes 
for inputs in body.find_all('div', {'class': 'input'}):
    inputs.replaceWith('')
    
# removes jupyter fonts and indents
for inputs in body.find_all('div', {'class': 'prompt input_prompt'}):
    inputs.replaceWith('')
for inputs in body.find_all('div', {'class': 'text_cell_render'}):
    inputs['class'].remove('text_cell_render')
for inputs in body.find_all('div', {'class': 'rendered_html'}):
    inputs['class'].remove('rendered_html')


# In[6]:


# gets shell
shell = open('shell.html', 'r')
shell_soup = BeautifulSoup(shell, 'html.parser')
shell.close()

# sets link to content css
shell_soup.find('link', {'id': 'custom'})['href'] = css_name

# sets title of post
shell_soup.find('a', {'id': 'post-title'}).string = title_name

# sets title of post
shell_soup.find('a', {'id': 'post-date'}).string = date

# sets content to content page
shell_soup.find('strong').replaceWith(body)


# In[7]:


# writes out css file
css = open('../' + css_name, 'w')
css.write(BeautifulSoup(style, 'html.parser').prettify())
css.close()

# writes out html file
html = open('../' + html_name, 'wb')
html.write(shell_soup.prettify().encode('utf8'))
html.close()

