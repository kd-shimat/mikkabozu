<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>各ページへのリンク</title>
    <ul>
        <?php
        # このディレクトリにあるdb*.phpのリストを取得しリンクを生成する
        foreach (glob('db*.php') as $file) {
            echo "<li><a href='{$file}'>{$file}</a></li>";
        }
        ?>
    </ul>
</head>
<body>

</body>
</html>
