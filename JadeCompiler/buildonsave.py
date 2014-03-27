import sublime, sublime_plugin, os, subprocess

class BuildingOnSave(sublime_plugin.EventListener):
	def on_post_save(self, view):
		savedFilePath = view.file_name()
		currentFolder = os.path.split(savedFilePath)[0]
		destFolder = os.path.split(os.path.split(savedFilePath)[0])[0] # Take off last two elements (filename and immediate dir) by splitting twice
		savedFileName = os.path.basename(savedFilePath)

		if sublime.platform() == 'osx':
			env = os.getenv('PATH')
			env += ':/usr/bin:/usr/local/bin:/usr/local/sbin'
			os.environ['PATH'] = env


		if savedFilePath.endswith('.jade'):
			isChildTemplate = view.substr(sublime.Region(0, 7)) == 'extends'

			if isChildTemplate:
				print('[JadeCompiler] Saved a child template - building.')
				self.compileJadeToHTML(savedFilePath, destFolder)

			else:
				print('[JadeCompiler] Saved a skeleton template - building all potential children.')

				for fileName in os.listdir(currentFolder):
					if fileName.endswith('.jade') and savedFilePath.find(fileName) == -1:
						self.compileJadeToHTML(os.path.join(currentFolder, fileName), destFolder)


	def compileJadeToHTML(self, filePath, destFolder):
		try:
			# not sure if node outputs on stderr or stdout so capture both
			p = subprocess.Popen(['jade', filePath, '--pretty', '--out', destFolder], stdout=subprocess.PIPE, stderr=subprocess.PIPE) # Calling the nitty gritty, manually
			print("[JadeCompiler] Built", filePath, "and saved to", destFolder + '/index.html')
		except OSError as err:
			# an error has occured, stop processing the file any further
			print(sublime.error_message('[JadeCompiler] error: ' + str(err)))
