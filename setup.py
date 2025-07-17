import setuptools
setuptools.setup(
	name='merge-effort',    
	version='1.1.1',
	license='MIT',
	url='XXXXX',
	author='XXXXXX',
	author_email='XXXXX@XXXX',
	description='a script to measure merge effort',
	packages= setuptools.find_packages(),
	entry_points={
		'console_scripts':[ 'merge-effort = mergeeffort.merge_analysis:main' ]
	},
	install_requires=[
        "pygit2>=0.27.0"
    ],

	)
