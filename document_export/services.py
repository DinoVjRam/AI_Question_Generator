from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors


class PDFExportService:

    @staticmethod
    def export_question_paper(paper, questions, file_path):

        doc = SimpleDocTemplate(file_path)

        styles = getSampleStyleSheet()

        # Custom styles
        title_style = ParagraphStyle(
            name="TitleStyle",
            fontSize=16,
            alignment=1,
            spaceAfter=10,
            textColor=colors.darkblue
        )

        normal_style = styles["Normal"]

        content = []

        # HEADER (University Style)
        content.append(Paragraph("AI QUESTION PAPER", title_style))
        content.append(Spacer(1, 10))

        # Paper Info
        meta = f"""
        <b>Course:</b> {paper.study_material.title}<br/>
        <b>Difficulty:</b> {paper.difficulty}<br/>
        <b>Bloom Level:</b> {paper.bloom_level}<br/>
        <b>Question Type:</b> {paper.question_type}<br/>
        <b>Total Questions:</b> {paper.total_questions}
        """

        content.append(Paragraph(meta, normal_style))
        content.append(Spacer(1, 20))

        # QUESTIONS
        content.append(Paragraph("<b>SECTION A</b>", normal_style))
        content.append(Spacer(1, 10))

        for q in questions:

            q_block = f"""
            <b>Q{q.sequence} ({q.marks} Marks)</b><br/>
            {q.question}<br/><br/>
            """

            content.append(Paragraph(q_block, normal_style))
            content.append(Spacer(1, 12))

        doc.build(content)

        return file_path