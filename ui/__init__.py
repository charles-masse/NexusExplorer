
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *

class HtmlDelegate(QStyledItemDelegate):

    def paint(self, painter, option, index):
        # Skip QTreeWidget topLevelItem to retain icons
        widget = option.widget
        if isinstance(widget, QTreeView) and not index.parent().isValid():
            super().paint(painter, option, index)
            return

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
