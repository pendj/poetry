/**
 * 诗歌创作平台主要JavaScript功能
 */

// 全局变量
const PoetryApp = {
    // 配置
    config: {
        apiBaseUrl: '/api',
        imageBaseUrl: '/static/images'
    },
    
    // 初始化
    init: function() {
        this.bindEvents();
        this.initTooltips();
        this.initSearch();
    },
    
    // 绑定事件
    bindEvents: function() {
        // 表单提交事件
        this.bindFormEvents();
        
        // 图片相关事件
        this.bindImageEvents();
        
        // 确认删除事件
        this.bindDeleteEvents();
    },
    
    // 表单事件
    bindFormEvents: function() {
        const forms = document.querySelectorAll('form[data-async]');
        forms.forEach(form => {
            form.addEventListener('submit', this.handleAsyncSubmit.bind(this));
        });
        
        // 诗词创建/编辑表单
        const poetryForms = document.querySelectorAll('#poetryForm, #editForm');
        poetryForms.forEach(form => {
            form.addEventListener('submit', this.handlePoetrySubmit.bind(this));
        });
    },
    
    // 图片事件
    bindImageEvents: function() {
        // 图片懒加载
        this.initLazyLoading();
        
        // 图片预览
        this.initImagePreview();
    },
    
    // 删除确认事件
    bindDeleteEvents: function() {
        const deleteLinks = document.querySelectorAll('a[href*="/delete"]');
        deleteLinks.forEach(link => {
            link.addEventListener('click', this.handleDeleteClick.bind(this));
        });
    },
    
    // 处理异步表单提交
    handleAsyncSubmit: function(e) {
        e.preventDefault();
        const form = e.target;
        const formData = new FormData(form);
        const submitBtn = form.querySelector('button[type="submit"]');
        
        // 显示加载状态
        this.setButtonLoading(submitBtn, true);
        
        fetch(form.action, {
            method: form.method,
            body: formData,
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                this.showMessage(data.message || '操作成功', 'success');
                if (data.redirect) {
                    window.location.href = data.redirect;
                }
            } else {
                this.showMessage(data.error || '操作失败', 'error');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            this.showMessage('网络错误，请重试', 'error');
        })
        .finally(() => {
            this.setButtonLoading(submitBtn, false);
        });
    },
    
    // 处理诗词表单提交
    handlePoetrySubmit: function(e) {
        const form = e.target;
        const submitBtn = form.querySelector('button[type="submit"]');
        const originalText = submitBtn.innerHTML;
        
        // 显示生成配图状态
        submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> 正在生成配图...';
        submitBtn.disabled = true;
        
        // 如果生成时间过长，恢复按钮状态
        setTimeout(() => {
            if (submitBtn.disabled) {
                submitBtn.innerHTML = originalText;
                submitBtn.disabled = false;
            }
        }, 30000);
    },
    
    // 处理删除点击
    handleDeleteClick: function(e) {
        e.preventDefault();
        const link = e.target.closest('a');
        const poetryTitle = link.dataset.title || '这首诗词';
        
        if (confirm(`确定要删除"${poetryTitle}"吗？此操作不可撤销。`)) {
            window.location.href = link.href;
        }
    },
    
    // 初始化搜索功能
    initSearch: function() {
        const searchInput = document.getElementById('searchInput');
        if (searchInput) {
            let searchTimeout;
            searchInput.addEventListener('input', function() {
                clearTimeout(searchTimeout);
                searchTimeout = setTimeout(() => {
                    const keyword = this.value.trim();
                    if (keyword.length > 0) {
                        PoetryApp.performSearch(keyword);
                    } else {
                        window.location.href = '/';
                    }
                }, 500);
            });
        }
    },
    
    // 执行搜索
    performSearch: function(keyword) {
        const url = new URL(window.location);
        url.searchParams.set('search', keyword);
        window.location.href = url.toString();
    },
    
    // 初始化图片懒加载
    initLazyLoading: function() {
        if ('IntersectionObserver' in window) {
            const imageObserver = new IntersectionObserver((entries, observer) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        const img = entry.target;
                        img.src = img.dataset.src;
                        img.classList.remove('lazy');
                        imageObserver.unobserve(img);
                    }
                });
            });
            
            document.querySelectorAll('img[data-src]').forEach(img => {
                imageObserver.observe(img);
            });
        }
    },
    
    // 初始化图片预览
    initImagePreview: function() {
        const images = document.querySelectorAll('.poetry-image');
        images.forEach(img => {
            img.addEventListener('click', function() {
                PoetryApp.showImageModal(this.src, this.alt);
            });
        });
    },
    
    // 显示图片模态框
    showImageModal: function(src, alt) {
        const modal = document.createElement('div');
        modal.className = 'image-modal';
        modal.innerHTML = `
            <div class="modal-backdrop" onclick="this.parentElement.remove()"></div>
            <div class="modal-content">
                <img src="${src}" alt="${alt}" class="modal-image">
                <button class="modal-close" onclick="this.closest('.image-modal').remove()">
                    <i class="fas fa-times"></i>
                </button>
            </div>
        `;
        
        // 添加样式
        const style = document.createElement('style');
        style.textContent = `
            .image-modal {
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                z-index: 9999;
                display: flex;
                align-items: center;
                justify-content: center;
            }
            .modal-backdrop {
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: rgba(0,0,0,0.8);
                cursor: pointer;
            }
            .modal-content {
                position: relative;
                max-width: 90%;
                max-height: 90%;
            }
            .modal-image {
                max-width: 100%;
                max-height: 100%;
                border-radius: 10px;
            }
            .modal-close {
                position: absolute;
                top: -40px;
                right: 0;
                background: rgba(255,255,255,0.9);
                border: none;
                border-radius: 50%;
                width: 40px;
                height: 40px;
                cursor: pointer;
                display: flex;
                align-items: center;
                justify-content: center;
            }
        `;
        
        document.head.appendChild(style);
        document.body.appendChild(modal);
    },
    
    // 初始化工具提示
    initTooltips: function() {
        const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        tooltipTriggerList.map(function (tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    },
    
    // 设置按钮加载状态
    setButtonLoading: function(button, loading) {
        if (loading) {
            button.dataset.originalText = button.innerHTML;
            button.innerHTML = '<i class="fas fa-spinner fa-spin"></i> 处理中...';
            button.disabled = true;
        } else {
            button.innerHTML = button.dataset.originalText || button.innerHTML;
            button.disabled = false;
        }
    },
    
    // 显示消息
    showMessage: function(message, type = 'info') {
        const alertClass = {
            'success': 'alert-success',
            'error': 'alert-danger',
            'warning': 'alert-warning',
            'info': 'alert-info'
        }[type] || 'alert-info';
        
        const alert = document.createElement('div');
        alert.className = `alert ${alertClass} alert-dismissible fade show`;
        alert.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        const container = document.querySelector('.container');
        container.insertBefore(alert, container.firstChild);
        
        // 自动消失
        setTimeout(() => {
            if (alert.parentNode) {
                alert.remove();
            }
        }, 5000);
    },
    
    // API调用
    api: {
        get: function(url) {
            return fetch(url).then(response => response.json());
        },
        
        post: function(url, data) {
            return fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            }).then(response => response.json());
        }
    }
};

// 页面加载完成后初始化
document.addEventListener('DOMContentLoaded', function() {
    PoetryApp.init();
});

// 导出到全局
window.PoetryApp = PoetryApp;
