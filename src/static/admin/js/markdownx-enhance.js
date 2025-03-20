// static/admin/js/markdownx-enhance.js
document.addEventListener('DOMContentLoaded', function() {
    const editor = document.querySelector('.markdownx-editor');
    if (!editor) return;
    
    const toolbar = document.createElement('div');
    toolbar.className = 'markdownx-toolbar';
    toolbar.style.marginBottom = '10px';
    
    const buttons = [
        { text: 'B', title: '粗体', action: () => insertAround('**', '**') },
        { text: 'I', title: '斜体', action: () => insertAround('*', '*') },
        { text: 'H2', title: '标题2', action: () => insertBefore('## ') },
        { text: 'H3', title: '标题3', action: () => insertBefore('### ') },
        { text: 'Link', title: '链接', action: () => insertAround('[', '](url)') },
        { text: 'Image', title: '图片', action: () => insertAround('![alt text](', ')') },
        { text: 'Code', title: '代码块', action: () => insertAround('```python\n', '\n```') },
        { text: 'List', title: '列表', action: () => insertBefore('- ') },
    ];
    
    buttons.forEach(btn => {
        const button = document.createElement('button');
        button.textContent = btn.text;
        button.title = btn.title;
        button.type = 'button';
        button.style.marginRight = '5px';
        button.style.padding = '3px 8px';
        button.addEventListener('click', btn.action);
        toolbar.appendChild(button);
    });
    
    editor.parentNode.insertBefore(toolbar, editor);
    
    function insertAround(before, after) {
        const start = editor.selectionStart;
        const end = editor.selectionEnd;
        const text = editor.value;
        const selected = text.substring(start, end);
        
        editor.value = text.substring(0, start) + before + selected + after + text.substring(end);
        editor.focus();
        editor.setSelectionRange(start + before.length, start + before.length + selected.length);
    }
    
    function insertBefore(text) {
        const start = editor.selectionStart;
        const lineStart = editor.value.lastIndexOf('\n', start - 1) + 1;
        
        editor.value = editor.value.substring(0, lineStart) + text + editor.value.substring(lineStart);
        editor.focus();
        editor.setSelectionRange(lineStart + text.length, lineStart + text.length);
    }
});

