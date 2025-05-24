
from PyQt6.QtGui import QColor, QPalette, QPainter, QTextDocument
from PyQt6.QtCore import Qt, QRect
from PyQt6.QtWidgets import QStyledItemDelegate, QStyle, QTreeView

class HtmlDelegate(QStyledItemDelegate):

    def paint(self, painter, option, index):
        
        widget = option.widget
        # Skip QTreeWidget topLevelItem to retain icons
        if isinstance(widget, QTreeView) and not index.parent().isValid():
            option_copy = option
            option_copy.state &= ~QStyle.StateFlag.State_Selected
            super().paint(painter, option_copy, index)

        else:
            painter.save()
            painter.setClipRect(option.rect)

            doc = QTextDocument(option.widget)
            doc.setDefaultFont(option.font)
            doc.setHtml(index.data())
            doc.setTextWidth(option.rect.width())
            doc.setDocumentMargin(0)

            context = doc.documentLayout().PaintContext()
            context.palette.setColor(QPalette.ColorRole.Text, QColor(125, 251, 182))

            if option.state & QStyle.StateFlag.State_MouseOver:
                painter.fillRect(option.rect, QColor(0, 100, 180, 50))

            if option.state & QStyle.StateFlag.State_Selected:
                painter.fillRect(option.rect, QColor(63, 126, 91, 255))

            painter.translate(option.rect.topLeft())
            
            doc.documentLayout().draw(painter, context)

            painter.restore()

    def sizeHint(self, option, index):

        doc = QTextDocument()
        doc.setDefaultFont(option.font)
        doc.setHtml(index.data())
        doc.setTextWidth(option.rect.width())
        doc.setDocumentMargin(0)

        return doc.size().toSize()
