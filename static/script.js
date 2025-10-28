$(function () {
  // 作家名が変更されたとき
  $("#author").change(function () {
    const url = $(this).val();
    const name = $("#author option:selected").text();

    if (url) {
      $.ajax({
        url: "/get_titles",
        type: "POST",
        contentType: "application/json",
        data: JSON.stringify({ url: url }),
        success: function (data) {
          $("#title").empty().append('<option value="">作品を選択してください</option>');
          data.forEach(function (title) {
            $("#title").append(`<option value="${title}">${title}</option>`);
          });
        },
        error: function (xhr, status, error) {
          console.error("作品一覧取得エラー:", error);
          alert("作品一覧の取得に失敗しました");
        }
      });
    } else {
      $("#title").empty().append('<option value="">先に作家を選んでください</option>');
    }
  });


  // 紹介文生成ボタンが押されたとき
  $("#generate").click(function () {
    const author = $("#author option:selected").text();
    const title = $("#title").val();

    if (!title) {
      alert("作品を選んでください");
      return;
    }

    $("#ai-result").text("AIによる詳細紹介を生成中...");

    // OpenAIによる紹介文
    $.ajax({
      url: "/generate_ai",
      type: "POST",
      contentType: "application/json",
      data: JSON.stringify({ author: author, title: title }),
      success: function (data) {
        $("#ai-result").text(data.result);
      },
      error: function (xhr, status, error) {
        console.error("AI生成エラー:", error);
        $("#ai-result").text("AIによる紹介文の生成に失敗しました");
      }
    });
  });
});