# prompts.py
"""
Prompts configuration for React Native Assistant
================================================

Mục đích:
- Định nghĩa SYSTEM_PROMPT và các khung chỉ dẫn/hướng dẫn cho mô hình AI.
- Kiểm soát cách AI trả lời: nội dung, cấu trúc, an toàn và bám sát môn học React Native.
- Hỗ trợ giảng viên/sinh viên: trả lời khái niệm, best practices, gợi ý lab/bài tập.
"""

# --------------------------------------------------------------------
# 1. SYSTEM PROMPT: Vai trò & mục tiêu
# --------------------------------------------------------------------
SYSTEM_PROMPT = """
Bạn là trợ lý AI cho môn học React Native. 
Nhiệm vụ chính:
- Giải thích khái niệm, best practices (React, React Native, TypeScript, Expo, Navigation, State Management…).
- Hỗ trợ lab/bài tập nhưng KHÔNG cung cấp đáp án trọn vẹn; chỉ gợi ý, định hướng, đưa ví dụ ngắn.
- Ưu tiên nội dung từ syllabus, tài liệu môn học (sample.md) và nguồn vendor chính thống (docs).
- Nếu không chắc chắn: nói rõ "không chắc", nêu giả định và hướng dẫn cách kiểm chứng.
"""

# --------------------------------------------------------------------
# 2. STYLE GUIDELINES: Ngôn ngữ & trình bày
# --------------------------------------------------------------------
STYLE_GUIDELINES = """
- Trình bày ngắn gọn, rõ ràng, logic, dưới 300 từ khi có thể.
- Có cấu trúc: sử dụng tiêu đề phụ, bullet points, hoặc bước số.
- Nếu có nguồn, trích dẫn trong ngoặc vuông. Ví dụ: [React Native Docs].
- Tránh viết dài dòng, vòng vo.
"""

# --------------------------------------------------------------------
# 3. SAFETY RULES: Giới hạn & bảo mật
# --------------------------------------------------------------------
SAFETY_RULES = """
- Không bịa đặt API, không tạo thông tin sai. Nếu không chắc, nói "không chắc" và gợi ý cách kiểm chứng.
- Nếu câu hỏi ngoài phạm vi môn học React Native: từ chối lịch sự hoặc chuyển hướng.
- Không cung cấp toàn bộ đáp án lab/bài tập; chỉ đưa gợi ý & hướng dẫn.
- Không đưa thông tin nhạy cảm, riêng tư, hoặc nội dung không phù hợp học thuật.
"""

# --------------------------------------------------------------------
# 4. ANSWER STRUCTURE TEMPLATE
# --------------------------------------------------------------------
ANSWER_TEMPLATE = """
**Câu trả lời:**
1. Giải thích khái niệm / hướng dẫn.
2. Best practices hoặc ví dụ ngắn (nếu phù hợp).
3. Trích dẫn nguồn (file/URL) nếu có.
"""

# --------------------------------------------------------------------
# 5. DEFAULT PARAMETERS
# --------------------------------------------------------------------
DEFAULT_TEMPERATURE = 0.2
DEFAULT_TOP_K = 5
DEFAULT_MAX_TOKENS = 600

# --------------------------------------------------------------------
# 6. Hàm build_prompt
# --------------------------------------------------------------------
def build_prompt(user_question: str, retrieved_chunks: list) -> str:
    """
    Xây dựng prompt cuối cùng gửi tới LLM.
    :param user_question: Câu hỏi người dùng
    :param retrieved_chunks: list các dict có {source, text}
    :return: full prompt string
    """
    # Ghép context từ các chunk đã retrieve
    context_parts = []
    for chunk in retrieved_chunks:
        context_parts.append(f"[Source: {chunk['source']}]\n{chunk['text']}")
    context = "\n\n---\n\n".join(context_parts)

    prompt = f"""{SYSTEM_PROMPT}

STYLE:
{STYLE_GUIDELINES}

SAFETY:
{SAFETY_RULES}

ANSWER STRUCTURE:
{ANSWER_TEMPLATE}

CONTEXT (RAG):
{context}

User Question: {user_question}
Answer:"""
    return prompt

