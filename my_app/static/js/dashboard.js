function toggleComments(postId) {
    const extraComments = document.querySelectorAll(`.extra-${postId}`);
    const toggleBtn = document.getElementById(`toggle-btn-${postId}`);

    if (!toggleBtn || extraComments.length === 0) {
        console.warn(`Elements missing for post ${postId}`);
        return;
    }

    const isHidden = extraComments[0].classList.contains('d-none');

    extraComments.forEach(comment => {
        comment.classList.toggle('d-none');
    });

    toggleBtn.textContent = isHidden ? 'See less' : 'See more';
}
