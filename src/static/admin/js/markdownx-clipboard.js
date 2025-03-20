(function() {
    // 等待DOM完全加载
    document.addEventListener('DOMContentLoaded', function() {
        setupClipboardImagePaste();
    });

    function setupClipboardImagePaste() {
        // 查找所有markdownx编辑器
        const editors = document.querySelectorAll('.markdownx-editor');
        
        editors.forEach(editor => {
            // 为每个编辑器添加粘贴事件监听器
            editor.addEventListener('paste', handlePaste);
        });
    }

    function handlePaste(e) {
        // 获取剪贴板数据
        const clipboardData = e.clipboardData || window.clipboardData;
        
        // 如果没有剪贴板数据，直接返回
        if (!clipboardData) return;
        
        // 检查剪贴板是否包含图片
        const items = clipboardData.items;
        
        if (!items) return;
        
        // 遍历剪贴板项目
        for (let i = 0; i < items.length; i++) {
            if (items[i].type.indexOf('image') !== -1) {
                // 阻止默认粘贴行为
                e.preventDefault();
                
                // 从剪贴板获取图片文件
                const file = items[i].getAsFile();
                
                if (!file) continue;
                
                // 上传图片
                uploadClipboardImage(file, this);
                
                // 找到一个图片后就退出循环
                break;
            }
        }
    }

    function uploadClipboardImage(file, editor) {
        // 显示上传状态
        const placeholder = `![正在上传图片...](uploading)`;
        const cursorPosition = editor.selectionStart;
        
        // 在光标位置插入占位符
        editor.value = 
            editor.value.substring(0, cursorPosition) + 
            placeholder + 
            editor.value.substring(cursorPosition);
        
        // 创建FormData对象用于上传
        const formData = new FormData();
        formData.append('image', file, 'clipboard-image-' + new Date().getTime() + '.png');
        
        // 获取CSRF token (Django需要)
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        
        // 发送AJAX请求
        fetch('/markdownx/upload/', {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': csrfToken
            },
            credentials: 'same-origin'
        })
        .then(response => response.json())
        .then(data => {
            if (data.image_code) {
                // 上传成功，替换占位符为实际图片链接
                const imageMarkdown = data.image_code;
                editor.value = editor.value.replace(placeholder, imageMarkdown);
                
                // 触发input事件以更新预览
                const event = new Event('input', {
                    'bubbles': true,
                    'cancelable': true
                });
                editor.dispatchEvent(event);
            } else {
                // 上传失败
                console.error('Image upload failed:', data);
                editor.value = editor.value.replace(placeholder, '![上传失败](error)');
                
                // 触发input事件以更新预览
                const event = new Event('input', {
                    'bubbles': true,
                    'cancelable': true
                });
                editor.dispatchEvent(event);
            }
        })
        .catch(error => {
            console.error('Error uploading image:', error);
            // 上传出错，替换占位符
            editor.value = editor.value.replace(placeholder, '![上传失败](error)');
            
            // 触发input事件以更新预览
            const event = new Event('input', {
                'bubbles': true,
                'cancelable': true
            });
            editor.dispatchEvent(event);
        });
    }
})();
function addPasteHint() {
    const editors = document.querySelectorAll('.markdownx-editor');
    
    editors.forEach(editor => {
        const hint = document.createElement('div');
        hint.className = 'markdownx-paste-hint';
        hint.textContent = '提示: 您可以直接粘贴图片 (Ctrl+V)';
        hint.style.fontSize = '12px';
        hint.style.color = '#666';
        hint.style.marginBottom = '5px';
        
        editor.parentNode.insertBefore(hint, editor);
    });
}

// 在DOMContentLoaded事件中调用
document.addEventListener('DOMContentLoaded', function() {
    setupClipboardImagePaste();
    addPasteHint();
});




