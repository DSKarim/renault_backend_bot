def get_progress_bar(percent):
    """
    Returns a text-based progress bar.
    Example: [███████░░░]
    """
    try:
        p = int(percent)
    except (ValueError, TypeError):
        return ""

    # Clamp between 0 and 100
    p = max(0, min(100, p))

    full_blocks = int(p / 10)
    empty_blocks = 10 - full_blocks

    return f"[{'█' * full_blocks}{'░' * empty_blocks}]"
