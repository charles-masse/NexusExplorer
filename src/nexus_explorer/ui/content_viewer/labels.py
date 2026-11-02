
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QLabel


class ContentLabel(QLabel):

    def __init__(self, text: str, name: str, icon: str | None = 'Caca'):
        super().__init__()

        self.icon = icon
        #Class name for stylesheet
        self.setObjectName(name)
        #Player input text
        if any(name.startswith(string) for string in ['LabelSay']):
            text = f'> <b>{text}</b>'

        self.setText(f'<div>{text.replace('\\n', '<br>')}</div>')
        self.setWordWrap(True)
        #Handle links
        self.setOpenExternalLinks(False)
        self.setTextInteractionFlags(Qt.TextInteractionFlag.TextBrowserInteraction)
        self.linkActivated.connect(self.popup)

        self.setFixedHeight(self.sizeHint().height())

    def popup(self, link):
        return link

#         modelId = eval(link)['creature2ModelInfoId']
#         modelPath = loadManager['Creature2ModelInfo'][modelId]['assetPath'].replace('.m3', '')
#         modelName = modelPath.split('\\')[-1]

#         scene = trimesh.load(f'{os.path.abspath(os.curdir)}/{settings['gameFiles']}/{modelPath}/{modelName}.gltf'.replace('\\', '/'))
#         scene.show()
