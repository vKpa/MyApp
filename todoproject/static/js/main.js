document.addEventListener('DOMContentLoaded', function() {
    // タスク完了状態の切り替え
    document.querySelectorAll('.toggle-complete').forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const taskId = this.dataset.taskId;
            const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

            fetch(`/task/${taskId}/toggle/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrftoken,
                    'Content-Type': 'application/json',
                },
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    const row = this.closest('tr');
                    row.classList.toggle('text-decoration-line-through');
                    this.textContent = data.completed ? '未対応にする' : '完了にする';
                }
            })
            .catch(error => console.error('Error:', error));
        });
    });

    // アラートの自動消去
    document.querySelectorAll('.alert').forEach(alert => {
        setTimeout(() => {
            alert.classList.remove('show');
            setTimeout(() => alert.remove(), 150);
        }, 3000);
    });
});

