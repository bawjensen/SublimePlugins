import sublime, sublime_plugin, os, subprocess

class BuildingOnSave(sublime_plugin.EventListener):
	def on_post_save(self, view):
		savedFilePath = view.file_name()
		savedFileName = os.path.basename(savedFilePath)

		if sublime.platform() == 'osx':
			env = os.getenv('PATH')
			env = env + ':/usr/bin:/usr/local/bin:/usr/local/sbin'
			os.environ['PATH'] = env


		if savedFilePath.endswith('.jade'):
			isChildTemplate = view.substr(sublime.Region(0, 7)) == 'extends'

			if isChildTemplate:
				print('[JadeCompiler] Saved a child template - building')
				self.compileJadeToHTML(savedFileName)

			else:
				print('[JadeCompiler] Saved a skeleton template - building self, then all...')
				self.compileJadeToHTML(savedFilePath)

				for fileName in os.listdir(folder):
					if fileName.endswith('.jade'):
						self.compileJadeToHTML(fileName)


	def compileJadeToHTML(self, fileName):
		# filePath = os.path.join(fileFolder, fileName)
		print('Building', fileName)
		try:
			# not sure if node outputs on stderr or stdout so capture both
			p = subprocess.Popen(['jade', fileName, '--pretty', '--out', '../'], stdout=subprocess.PIPE, stderr=subprocess.PIPE) # Calling the nitty gritty, manually
		except OSError as err:
			# an error has occured, stop processing the file any further
			print(sublime.error_message('[JadeCompiler] error: ' + str(err)))
